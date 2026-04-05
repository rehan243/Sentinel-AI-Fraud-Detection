"""Model Drift Monitor for Fraud Detection - Rehan Malik"""

import numpy as np
from dataclasses import dataclass


@dataclass
class DriftAlert:
    feature: str
    psi_score: float
    severity: str
    action: str


class FraudModelMonitor:
    def __init__(self, features: list[str], threshold: float = 0.2):
        self.features = features
        self.threshold = threshold
        self.reference = None

    def set_reference(self, data: np.ndarray):
        self.reference = data

    def compute_psi(self, ref: np.ndarray, cur: np.ndarray, bins: int = 10) -> float:
        eps = 1e-6
        breaks = np.percentile(ref, np.linspace(0, 100, bins + 1))
        breaks = np.unique(breaks)
        ref_pct = np.histogram(ref, bins=breaks)[0] / len(ref) + eps
        cur_pct = np.histogram(cur, bins=breaks)[0] / len(cur) + eps
        return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))

    def check(self, current: np.ndarray) -> list[DriftAlert]:
        alerts = []
        for i, feat in enumerate(self.features):
            psi = self.compute_psi(self.reference[:, i], current[:, i])
            if psi >= 0.5:
                severity, action = "critical", "retrain_immediately"
            elif psi >= self.threshold:
                severity, action = "high", "schedule_retrain"
            elif psi >= 0.1:
                severity, action = "medium", "monitor"
            else:
                severity, action = "low", "none"
            alerts.append(DriftAlert(feat, round(psi, 4), severity, action))
        return alerts


if __name__ == "__main__":
    np.random.seed(42)
    features = ["amount", "velocity", "hour", "distance"]
    monitor = FraudModelMonitor(features)
    monitor.set_reference(np.random.randn(1000, 4))
    current = np.random.randn(500, 4) + np.array([0, 0.5, 0, 1.0])
    for alert in monitor.check(current):
        print(f"[{alert.severity.upper()}] {alert.feature}: PSI={alert.psi_score} -> {alert.action}")
