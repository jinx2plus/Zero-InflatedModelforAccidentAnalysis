# Upload Review (Final)

이 폴더(`release_upload/`)는 GitHub 업로드용으로 분리한 최종본입니다.

## 포함 파일 목록
- `.gitignore`
- `.env.example`
- `README.md`
- `requirements.txt`
- `train_model.py`
- `docs/research_summary.md`
- `data/README.md`
- `results/feature_importance_VERSION1.csv`
- `results/feature_importance_VERSION2.csv`

## 검토 결과
1. 민감정보 점검
- 키워드 기반 점검(`password`, `token`, `api_key`, DB URL/계정, 로컬 사용자 경로 등)에서 **매치 없음**.

2. 결과 파일 형식 점검
- `results/feature_importance_VERSION1.csv`: 20행, 컬럼 `Feature, Importance`
- `results/feature_importance_VERSION2.csv`: 20행, 컬럼 `Feature, Importance`
- 불필요한 노트 행(`Note:`) 없음.

3. 문서 연결 점검
- `README.md`에서 안내한 주요 문서/코드 파일 실제 존재 확인.

## 최종 판단
- 공개 저장소 업로드 기준으로 **이상 징후 없음**.
- 원본 데이터/노트북/문서 초안(`.docx`, `.ipynb`, `.zip`)은 본 폴더에 포함되지 않음.

## 업로드 방법
`release_upload/` 폴더에서 아래 실행:

```bash
git init
git add .
git commit -m "Initial public release"
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```
