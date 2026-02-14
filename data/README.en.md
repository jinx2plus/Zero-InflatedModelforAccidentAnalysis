# Data Folder Policy

Keep only public-safe sample or explanatory files in this folder.

- Do not commit raw accident data files (Excel/DB exports).
- Do not commit files containing personal data, internal identifiers, or connection credentials.
- Inject the real dataset path at runtime via CLI (`--data-path`) or `DATA_FILE` environment variable.
