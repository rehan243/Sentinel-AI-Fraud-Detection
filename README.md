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

---

> **Source Code**: The production source code for this project is maintained in a private repository due to proprietary and client confidentiality requirements. This repository documents the architecture, design decisions, and technical approach. For code-level discussions or collaboration inquiries, feel free to reach out.


## Author

**Rehan Malik** — Senior AI/ML Engineer @ Reallytics.ai

- [LinkedIn](https://linkedin.com/in/rehan-malik-62b3301ab)
- [GitHub](https://github.com/rehan243)
- [Live Demo](https://fraud-detection.reallytics.ai)

---