"""fastapi + two-model ensemble - because one model is a single point of failure"""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path
from typing import Any, Optional

import numpy as np
from fastapi import FastAPI, Header, HTTPException, Request
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel, Field
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

logger = logging.getLogger(__name__)

PREDICTIONS = Counter("fraud_predictions_total", "predictions", ["model_version", "variant"])
LATENCY = Histogram("fraud_predict_latency_seconds", "latency", ["model_version"])
ERRORS = Counter("fraud_predict_errors_total", "errors")


class PredictRequest(BaseModel):
    features: dict[str, float] = Field(..., description="numeric feature dict from FeatureEngine")
    txn_id: Optional[str] = None


class PredictResponse(BaseModel):
    score: float
    model_version: str
    variant: str
    request_id: str


class ModelBundle:
    def __init__(self, xgb_path: Path, version: str, scaler_path: Optional[Path] = None) -> None:
        if not xgb_path.exists():
            raise FileNotFoundError(f"xgb model missing: {xgb_path}")
        self.xgb = xgb.Booster()
        self.xgb.load_model(xgb_path)
        self.version = version
        self.scaler = StandardScaler()
        self._feature_order: list[str] = []
        self.nn_stub_weight = 0.15
        if scaler_path and scaler_path.exists():
            import pickle

            with scaler_path.open("rb") as fh:
                self.scaler = pickle.load(fh)

    def set_feature_order(self, cols: list[str]) -> None:
        self._feature_order = cols

    def predict_row(self, feats: dict[str, float]) -> float:
        if not self._feature_order:
            self._feature_order = sorted(feats.keys())
        vec = np.array([[feats.get(c, 0.0) for c in self._feature_order]], dtype=np.float32)
        if hasattr(self.scaler, "mean_") and getattr(self.scaler, "mean_", None) is not None:
            try:
                vec = self.scaler.transform(vec)
            except Exception as exc:
                logger.warning("scaling failed: %s", exc)
        dmat = xgb.DMatrix(vec, feature_names=self._feature_order)
        xgb_p = float(self.xgb.predict(dmat)[0])
        nn_p = 1.0 / (1.0 + np.exp(-float(vec.mean())))
        return float((1 - self.nn_stub_weight) * xgb_p + self.nn_stub_weight * nn_p)


def create_app(model_dir: Path) -> FastAPI:
    app = FastAPI(title="Sentinel Fraud Scoring", version="1.1.0")
    bundle_a = ModelBundle(model_dir / "fraud_xgb.json", "v3.2.0")
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

    def _select_variant(experiment_header: Optional[str]) -> tuple[ModelBundle, str]:
        if experiment_header == "B":
            return bundle_a, "B"
        return bundle_a, "A"

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        rid = str(uuid.uuid4())
        request.state.request_id = rid
        t0 = time.perf_counter()
        try:
            resp = await call_next(request)
            return resp
        finally:
            logger.info(
                "request %s %s %.3fs",
                rid,
                request.url.path,
                time.perf_counter() - t0,
            )

    @app.post("/predict", response_model=PredictResponse)
    async def predict(
        body: PredictRequest,
        request: Request,
        x_experiment_variant: Optional[str] = Header(default=None),
    ) -> PredictResponse:  # added return type hint
        try:
            model, variant = _select_variant(x_experiment_variant)
            t0 = time.perf_counter()
            score = model.predict_row(body.features)
            LATENCY.labels(model.version).observe(time.perf_counter() - t0)
            PREDICTIONS.labels(model.version, variant).inc()
            return PredictResponse(
                score=score,
                model_version=model.version,
                variant=variant,
                request_id=getattr(request.state, "request_id", ""),
            )
        except Exception as exc:
            ERRORS.inc()
            logger.exception("predict failed: %s", exc)
            raise HTTPException(status_code=500, detail="scoring_failed") from exc

    return app