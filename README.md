# Zero-Inflated Model for Accident Analysis

졸음쉼터 설치 전/후 교통사고 건수 데이터를 대상으로 Zero-Inflated Negative Binomial(ZINB) 딥러닝 모델을 학습하고,
Permutation Importance로 영향 변수를 분석한 프로젝트입니다.

## 공개용 정리 기준
- 원본 데이터 파일(엑셀), 노트북 출력, 문서 초안(`.docx`), 압축본(`.zip`)은 기본적으로 Git 추적에서 제외합니다.
- 실행 가능한 코드와 연구 결과 요약, 결과 CSV만 공개 대상으로 유지합니다.

## 폴더 구조
```text
.
├─ train_model.py
├─ requirements.txt
├─ .env.example
├─ results/
│  ├─ feature_importance_VERSION1.csv
│  └─ feature_importance_VERSION2.csv
├─ docs/
│  └─ research_summary.md
├─ data/
│  └─ README.md
└─ .gitignore
```

## 실행 방법
1. 의존성 설치
```bash
pip install -r requirements.txt
```

2. 학습 실행
```bash
python train_model.py --data-path "<your_excel_path>" --output-dir results
```

또는 `.env.example`을 참고하여 `DATA_FILE` 환경변수로 경로를 전달할 수 있습니다.

선택 옵션:
- `--versions VERSION1 VERSION2`
- `--epochs 500`
- `--learning-rate 0.001`

## 핵심 결과(요약)
- Version1 상위 변수: `연속주행시간`, `통행속도`, `2시간 이상 주행차량 대수`
- Version2 상위 변수: `톨게이트(개수)`, `통행속도`, `차로수`
- `Is_After` 중요도는 두 버전 모두 낮거나 음수로 나타나, 설치 전후 구분 변수 자체보다 도로/통행 특성 변수가 상대적으로 더 크게 작용했습니다.

자세한 내용은 `docs/research_summary.md`를 참고하세요.

## 별도 GitHub 저장소 업로드 예시
```bash
git init
git add .
git commit -m "Initial public release"
```

원격 저장소 연결 후:
```bash
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```
