import argparse
import os
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


DEFAULT_VERSIONS = ("VERSION1", "VERSION2")


class ZINBModel(nn.Module):
    def __init__(self, input_dim: int) -> None:
        super().__init__()

        self.shared = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
        )
        self.pi_head = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )
        self.mu_head = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Softplus(),
        )
        self.theta_head = nn.Sequential(
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Softplus(),
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        shared_out = self.shared(x)
        pi_logit = self.pi_head(shared_out)
        mu = self.mu_head(shared_out) + 1e-6
        theta = self.theta_head(shared_out) + 1e-6
        return pi_logit, mu, theta


def zinb_loss(
    y_true: torch.Tensor,
    pi_logit: torch.Tensor,
    mu: torch.Tensor,
    theta: torch.Tensor,
) -> torch.Tensor:
    pi = torch.sigmoid(pi_logit)
    eps = 1e-8

    nb_zero_prob = (theta / (theta + mu)).pow(theta)
    prob_zero = pi + (1 - pi) * nb_zero_prob
    loss_zero = -torch.log(prob_zero + eps)

    log_nb_y = (
        torch.lgamma(y_true + theta)
        - torch.lgamma(y_true + 1)
        - torch.lgamma(theta)
        + theta * (torch.log(theta) - torch.log(theta + mu))
        + y_true * (torch.log(mu) - torch.log(theta + mu))
    )
    loss_nonzero = -(torch.log(1 - pi + eps) + log_nb_y)

    mask_zero = (y_true == 0).float()
    loss = mask_zero * loss_zero + (1 - mask_zero) * loss_nonzero
    return loss.mean()


def load_and_process_data(file_path: str, version: str) -> Tuple[pd.DataFrame, np.ndarray]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    df = pd.read_excel(file_path)
    target_before = f"ACCIDENTS_BEFOREINSTALLATION_{version}"
    target_after = f"ACCIDENTS_AFTERINSTALLATION_{version}"

    missing_targets = [c for c in (target_before, target_after) if c not in df.columns]
    if missing_targets:
        raise KeyError(f"Missing target columns for {version}: {missing_targets}")

    other_targets = [
        c for c in df.columns if "ACCIDENTS_" in c and c not in (target_before, target_after)
    ]
    drop_cols = ["FID", "Shape", "ROADNAME", "EMD_CD", "ACCIDENTS", *other_targets]
    df_features = df.drop(columns=drop_cols, errors="ignore")

    y_before = df[target_before].to_numpy()
    y_after = df[target_after].to_numpy()
    x_base = df_features.drop(columns=[target_before, target_after], errors="ignore")
    x_base = x_base.drop(columns=["ROADNO"], errors="ignore")

    x_before = x_base.copy()
    x_before["Is_After"] = 0
    x_after = x_base.copy()
    x_after["Is_After"] = 1

    x = pd.concat([x_before, x_after], ignore_index=True)
    y = np.concatenate([y_before, y_after])
    return x, y


def train_single_version(
    file_path: str,
    version: str,
    output_dir: Path,
    epochs: int,
    learning_rate: float,
) -> pd.DataFrame:
    print(f"\n--- Training ZINB model for {version} ---")
    x, y = load_and_process_data(file_path, version)

    print(f"Data shape: {x.shape}, Target shape: {y.shape}")
    print(f"Zero percentage in target: {(y == 0).mean() * 100:.2f}%")

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    x_train_tensor = torch.tensor(x_train_scaled, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    x_test_tensor = torch.tensor(x_test_scaled, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    model = ZINBModel(input_dim=x_train.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        pi_logit, mu, theta = model(x_train_tensor)
        loss = zinb_loss(y_train_tensor, pi_logit, mu, theta)
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}")

    model.eval()
    with torch.no_grad():
        pi_logit, mu, theta = model(x_test_tensor)
        test_loss = zinb_loss(y_test_tensor, pi_logit, mu, theta)
        pi = torch.sigmoid(pi_logit)
        y_pred = (1 - pi) * mu
        mse = torch.mean((y_pred - y_test_tensor) ** 2)

    print(f"Final test loss: {test_loss.item():.4f}")
    print(f"Test MSE: {mse.item():.4f}")

    print("Calculating permutation feature importance...")
    base_loss = test_loss.item()
    feature_names = x.columns.tolist()
    importances: List[Dict[str, object]] = []

    for idx, col in enumerate(feature_names):
        x_test_permuted = x_test_tensor.clone()
        perm_idx = torch.randperm(x_test_tensor.size(0))
        x_test_permuted[:, idx] = x_test_tensor[perm_idx, idx]

        with torch.no_grad():
            pi_logit_p, mu_p, theta_p = model(x_test_permuted)
            loss_p = zinb_loss(y_test_tensor, pi_logit_p, mu_p, theta_p).item()

        importances.append({"Feature": col, "Importance": round(loss_p - base_loss, 6)})

    importance_df = pd.DataFrame(importances).sort_values(by="Importance", ascending=False)
    output_file = output_dir / f"feature_importance_{version}.csv"
    importance_df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Saved: {output_file}")
    print(importance_df.head(10).to_string(index=False))
    return importance_df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Zero-Inflated Negative Binomial model.")
    parser.add_argument(
        "--data-path",
        default=os.getenv("DATA_FILE"),
        help="Path to input Excel file. You can also set DATA_FILE env var.",
    )
    parser.add_argument(
        "--versions",
        nargs="+",
        default=list(DEFAULT_VERSIONS),
        help="Target versions to train (default: VERSION1 VERSION2).",
    )
    parser.add_argument("--epochs", type=int, default=500, help="Training epochs (default: 500).")
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=1e-3,
        help="Learning rate for Adam optimizer (default: 0.001).",
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory to save feature importance CSV files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.data_path:
        raise ValueError("Missing --data-path (or DATA_FILE environment variable).")

    torch.manual_seed(42)
    np.random.seed(42)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for version in args.versions:
        train_single_version(
            file_path=args.data_path,
            version=version,
            output_dir=output_dir,
            epochs=args.epochs,
            learning_rate=args.learning_rate,
        )


if __name__ == "__main__":
    main()

