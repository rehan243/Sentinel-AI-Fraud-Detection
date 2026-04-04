# Sentinel AI — Fraud Detection Co-Pilot

The first AI Co-Pilot that stops fraud and explains why. Real-time fraud detection with explainable AI for financial institutions.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=flat-square)](https://xgboost.ai)

[Live Demo](https://fraud-detection.reallytics.ai)

---

## Overview

Production-grade AI fraud detection platform deployed for financial institutions, lending platforms, and fintech companies. Sentinel AI acts as an intelligent ride-along partner for fraud review teams, providing real-time fraud probability scores (0.0–1.0) and plain-English explanations powered by GenAI.

Built at **Reallytics.ai** for Tower Loan and other financial services clients.

## Architecture

`
┌──────────────────────────────────────────────────────┐
│              Data Integration Layer                    │
│  OLL/TLOS Loan Application Systems                    │
│  - Secure data ingestion                              │
│  - Encrypted PII handling                             │
│  - ~100 raw data points per application               │
└─────────────────────────┬────────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────────┐
│          Feature Engineering Pipeline                  │
│  - 650+ predictive features generated                 │
│  - Behavioral anomaly detection (deltaH timing)       │
│  - Contact information pattern analysis               │
│  - Profile stability scoring                          │
│  - Identity verification signals                      │
└─────────────────────────┬────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │                               │
┌─────────▼──────────┐  ┌────────────────▼───────────┐
│  XGBoost Detective │  │  Isolation Forest Watchdog  │
│  (Supervised)      │  │  (Unsupervised)             │
│  - Known fraud     │  │  - Novel fraud patterns     │
│    patterns        │  │  - Mathematical anomaly     │
│  - 25% recall      │  │    profiling                │
└─────────┬──────────┘  └────────────────┬───────────┘
          │                               │
┌─────────▼───────────────────────────────▼───────────┐
│              Ensemble  Task Force (50/50)            │
│  Combined score → 50% fraud detection on holdout     │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│          Persona Classification (UMAP + HDBSCAN)     │
│  - Digital Ghost (70% fraud concentration)           │
│  - High-Friction Anomaly (abnormally slow process)   │
│  - Safe Bet (100% legitimate, fast-track)            │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│         GenAI Explanation Engine (Amazon Bedrock)     │
│  - SHAP value interpretation                         │
│  - Plain-English PDF reports                         │
│  - Risk factors + mitigating factors                 │
└─────────────────────────────────────────────────────┘
`

## Key Features

- **Ensemble Detection**: Task Force combining XGBoost (supervised, known patterns) + Isolation Forest (unsupervised, novel fraud) — 50% fraud detection on holdout
- **650+ Engineered Features**: Behavioral anomalies, timing patterns, contact signals, identity verification, profile stability
- **3 Applicant Personas**: Unsupervised UMAP + HDBSCAN reveals Digital Ghost (70% fraud), High-Friction Anomaly, and Safe Bet personas
- **Explainable AI**: GenAI-powered PDF reports via Amazon Bedrock translating SHAP values into plain English
- **Real-Time Scoring**: Headless API on AWS Lambda/SageMaker with API Gateway — scores applications at pre-funding stage
- **Fraud Indicators**: Detects early reversals, legal actions, repos, UCC failures, forgeries, first-payment defaults
- **Continuous Learning**: Automated retraining pipelines with data drift detection and A/B model deployment

## Tech Stack

| Category | Technologies |
|---|---|
| **ML Models** | XGBoost, Isolation Forest, UMAP, HDBSCAN |
| **Feature Engineering** | Python, Pandas, NumPy, scikit-learn |
| **Explainability** | SHAP, Amazon Bedrock (GenAI reports) |
| **Cloud** | AWS Lambda, SageMaker, API Gateway, S3 |
| **Data** | PostgreSQL, encrypted PII handling |
| **MLOps** | CloudWatch, QuickSight, automated retraining |
| **API** | FastAPI, REST endpoints |

## Project Structure

`
sentinel-ai-fraud-detection/
├── data/
│   ├── ingestion/
│   │   ├── oll_connector.py
│   │   ├── tlos_connector.py
│   │   └── pii_encryption.py
│   └── feature_engineering/
│       ├── behavioral_features.py
│       ├── contact_features.py
│       ├── identity_features.py
│       └── timing_features.py
├── models/
│   ├── xgboost_detective.py
│   ├── isolation_forest_watchdog.py
│   ├── ensemble_task_force.py
│   └── persona_classifier.py
├── explainability/
│   ├── shap_analyzer.py
│   ├── bedrock_report_generator.py
│   └── pdf_builder.py
├── api/
│   ├── main.py
│   ├── scoring_endpoint.py
│   └── report_endpoint.py
├── mlops/
│   ├── drift_detector.py
│   ├── retraining_pipeline.py
│   └── model_registry.py
├── infrastructure/
│   ├── Dockerfile
│   ├── sagemaker_deploy.py
│   └── lambda_handler.py
├── tests/
├── requirements.txt
└── README.md
`

## Results

| Metric | Value |
|---|---|
| Fraud detection rate (holdout) | 50% |
| Features engineered | 650+ |
| Applicant personas discovered | 3 |
| XGBoost recall | 25% |
| Ensemble improvement | 2x over single model |
| Scoring latency | < 500ms |
| False positive rate | < 15% |

## Industries Served

- Financial Institutions
- Lending Platforms
- Credit Unions
- Online Lenders
- Fintech Companies

## Quick Start

`ash
git clone https://github.com/rehan243/Sentinel-AI-Fraud-Detection.git
cd Sentinel-AI-Fraud-Detection

pip install -r requirements.txt

# Feature engineering
python data/feature_engineering/behavioral_features.py --input ./data/raw

# Train ensemble
python models/ensemble_task_force.py --config configs/training.yaml

# Start scoring API
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Generate explainable report
python explainability/bedrock_report_generator.py --application-id LA-2024-1248
`

## Author

**Rehan Malik** — Senior AI/ML Engineer @ Reallytics.ai

- [LinkedIn](https://linkedin.com/in/rehan-malik-62b3301ab)
- [GitHub](https://github.com/rehan243)
- [Live Demo](https://fraud-detection.reallytics.ai)

---

