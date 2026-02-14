# Research Summary

## 1) Objective
Identify variables associated with traffic accident counts before and after drowsy rest area installation, and evaluate the relative importance of the before/after indicator (`Is_After`).

## 2) Method
- Model: Zero-Inflated Negative Binomial (ZINB) Neural Network
- Targets: `ACCIDENTS_BEFOREINSTALLATION_VERSION*`, `ACCIDENTS_AFTERINSTALLATION_VERSION*`
- Data construction: stack before/after observations with `Is_After` flag (0/1)
- Training/Evaluation: train-test split, minimize ZINB negative log-likelihood
- Variable importance: permutation importance (increase in loss)

## 3) Results
### Version1 Top 10
| Rank | Feature | Importance |
|---|---|---:|
| 1 | Continuous driving time (`연속주행시간`) | 1.05 |
| 2 | Travel speed (`통행속도`) | 0.60 |
| 3 | Vehicles driving over 2 hours (`2시간 이상 주행차량 대수`) | 0.57 |
| 4 | Average speed (`평균속도`) | 0.55 |
| 5 | Continuous driving time index (`연속주행시간 지수`) | 0.47 |
| 6 | Top 1% avg continuous driving time (`연속주행시간 상위 1% 평균`) | 0.44 |
| 7 | Ratio of vehicles driving over 2 hours (`2시간 이상 주행차량 비율`) | 0.43 |
| 8 | Number of tollgates (`톨게이트(개수)`) | 0.41 |
| 9 | Mean curve radius (`곡선반경(평균)`) | 0.33 |
| 10 | IC: at-grade/interchange count (`IC(분기점,일반국도와 일반국도 간 입체교차로)`) | 0.32 |

### Version2 Top 10
| Rank | Feature | Importance |
|---|---|---:|
| 1 | Number of tollgates (`톨게이트(개수)`) | 0.85 |
| 2 | Travel speed (`통행속도`) | 0.67 |
| 3 | Number of lanes (`차로수`) | 0.65 |
| 4 | Average speed (`평균속도`) | 0.50 |
| 5 | IC: at-grade/interchange count (`IC(분기점,일반국도와 일반국도 간 입체교차로)`) | 0.50 |
| 6 | Continuous driving time (`연속주행시간`) | 0.48 |
| 7 | Sum of curve radius (`곡선반경(합계)`) | 0.36 |
| 8 | Continuous driving time index (`연속주행시간 지수`) | 0.28 |
| 9 | Bus-only lane flag (`버스전용차로유무`) | 0.27 |
| 10 | Vehicles driving over 2 hours (`2시간 이상 주행차량 대수`) | 0.24 |

## 4) Interpretation Points
- Across both versions, speed/continuous-driving/road-structure variables (lanes, tollgates, curve radius) are consistently ranked high.
- `Is_After` importance is low or negative (Version1: -0.13, Version2: -0.05).
  - This suggests road and traffic features contributed more directly to model loss than the before/after indicator itself.
- Importance values are predictive relevance, not direct causal proof.

## 5) Reproducibility Notes
- Do not include raw source data in the public repository.
- Provide data file path via `--data-path` or `DATA_FILE` environment variable.
- Save output CSV files under `results/`.
