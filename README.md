# Traffic Accident Risk Modeling (Zero-Inflated Approach)
# 교통사고 위험도 모델링 (Zero-Inflated 모델 기반)

Applied statistical modeling for real-world traffic accident analysis  
using Zero-Inflated count models.

Zero-Inflated 계수형 통계 모델을 활용한  
실제 교통사고 데이터 기반 위험도 분석 프로젝트입니다.

---

## 🚀 Project Overview | 프로젝트 개요

This repository implements a Zero-Inflated modeling framework  
to analyze accident frequency and severity in transportation networks.

본 레포지토리는 교통망 내 사고 발생 빈도 및 심각도를 분석하기 위한  
Zero-Inflated 모델링 프레임워크를 구현합니다.

It is designed for:
- Traffic safety policy analysis  
- Risk hotspot identification  
- Mobility service planning  

적용 목적:
- 교통안전 정책 수립 지원  
- 사고 다발 구간 도출  
- 모빌리티 서비스 운영 전략 수립  

---

## ⚙️ Why Zero-Inflated? | Zero-Inflated 모델을 사용하는 이유

Traffic accident data typically contains excess zeros  
(many locations with no accidents).

교통사고 데이터는 사고가 발생하지 않은 지점이 많아  
과잉 0 (excess zero) 특성을 가집니다.

Zero-Inflated models:
- Separate structural zeros from sampling zeros  
- Improve model fit for sparse count data  
- Provide interpretable risk estimation  

Zero-Inflated 모델은:
- 구조적 0과 확률적 0을 분리  
- 희소 계수 데이터 적합도 개선  
- 해석 가능한 위험도 추정 가능  

---

## 📊 Core Methodology | 주요 분석 방법

1. Data preprocessing & feature engineering  
2. Count distribution diagnostics  
3. Zero-Inflated Poisson / Negative Binomial modeling  
4. Model comparison & validation  
5. Risk zone visualization  


1. 데이터 전처리 및 변수 설계  
2. 분포 진단  
3. ZIP / ZINB 모델 구축  
4. 모델 비교 및 검증  
5. 위험 지역 시각화  

---

## 📈 Key Outputs | 주요 산출물

- Accident frequency prediction  
- High-risk spatial clusters  
- Policy-supportive interpretability  

- 사고 발생 확률 예측  
- 고위험 공간 군집 도출  
- 정책 적용 가능한 해석 결과  

---

## 🧠 Business Relevance | 사업적 활용성

This project demonstrates the ability to:

- Apply advanced statistical models to transportation data  
- Translate model outputs into actionable mobility insights  
- Support public-sector & mobility platform decisions  

본 프로젝트는 다음 역량을 증명합니다:

- 교통 데이터에 대한 고급 통계 모델 적용 능력  
- 분석 결과를 실무 의사결정 인사이트로 전환  
- 공공 및 모빌리티 플랫폼 의사결정 지원 가능  


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

1. 학습 실행

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

---

## English

This project trains a Zero-Inflated Negative Binomial (ZINB) deep learning model on traffic accident count data before and after drowsy rest area installation, and analyzes influential variables using permutation importance.

### Public Release Scope

- Raw data files (Excel), notebook outputs, draft documents (`.docx`), and archives (`.zip`) are excluded from Git tracking by default.
- Only executable code, research summary documents, and curated result CSV files are included for public release.

### Folder Structure

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

### How to Run

1. Run training

```bash
python train_model.py --data-path "<your_excel_path>" --output-dir results
```

You can also provide the data path via the `DATA_FILE` environment variable (see `.env.example`).

Optional arguments:

- `--versions VERSION1 VERSION2`
- `--epochs 500`
- `--learning-rate 0.001`

### Key Results (Summary)

- Top variables in Version1: `Continuous Driving Time`, `Travel Speed`, `Number of Vehicles Driving Over 2 Hours`
- Top variables in Version2: `Toll Gates (Count)`, `Travel Speed`, `Number of Lanes`
- `Is_After` importance is low or negative in both versions, suggesting road/traffic features contributed more strongly than the before/after indicator itself.

For details, see `docs/research_summary.md`.
