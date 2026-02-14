# Zero-Inflated Model for Accident Analysis

This project trains a Zero-Inflated Negative Binomial (ZINB) deep learning model on traffic accident count data before and after drowsy rest area installation, and analyzes influential variables using permutation importance.

## Public Release Scope
- Raw data files (Excel), notebook outputs, draft documents (`.docx`), and archives (`.zip`) are excluded from Git tracking by default.
- Only executable code, research summary documents, and curated result CSV files are included for public release.

## Folder Structure
```text
.
├─ train_model.py
├─ requirements.txt
├─ .env.example
├─ results/
│  ├─ feature_importance_VERSION1.csv
│  └─ feature_importance_VERSION2.csv
├─ docs/
│  ├─ research_summary.md
│  └─ research_summary.en.md
├─ data/
│  ├─ README.md
│  └─ README.en.md
└─ .gitignore
```

## How to Run
1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Run training
```bash
python train_model.py --data-path "<your_excel_path>" --output-dir results
```

You can also pass the path through the `DATA_FILE` environment variable (see `.env.example`).

Optional arguments:
- `--versions VERSION1 VERSION2`
- `--epochs 500`
- `--learning-rate 0.001`

## Key Results (Summary)
- Top variables in Version1: `연속주행시간`, `통행속도`, `2시간 이상 주행차량 대수`
- Top variables in Version2: `톨게이트(개수)`, `통행속도`, `차로수`
- `Is_After` importance is low or negative in both versions, suggesting road/traffic features contributed more strongly than the before/after indicator itself.

For details, see `docs/research_summary.md` and `docs/research_summary.en.md`.

## Example: Upload to a Separate GitHub Repository
```bash
git init
git add .
git commit -m "Initial public release"
```

After connecting a remote repository:
```bash
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```
