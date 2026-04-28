"""Real-time-ish features — Redis-backed windows because PostgreSQL will cry."""

from __future__ import annotations

import hashlib
import logging
import math
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Optional

import numpy as np
import redis

logger = logging.getLogger(__name__)

# MCC risk: toy prior — replace with your compliance team's spreadsheet
_MCC_RISK: dict[str, float] = {
    "5411": 0.2,
    "5960": 0.85,
    "7995": 0.95,
    "4829": 0.7,
}


@dataclass
class TransactionEvent:
    txn_id: str
    customer_id: str
    amount: float
    currency: str
    merchant_id: str
    mcc: str
    lat: float
    lon: float
    device_fp: str
    ts: float = field(default_factory=time.time)


class FeatureEngine:
    """Velocity + amount deviation + geo + device. Inject Redis client for tests."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        redis_client: Optional[redis.Redis] = None,
    ) -> None:
        self.r = redis_client or redis.from_url(redis_url, decode_responses=True)
        self._local_rollups: dict[str, Deque[tuple[float, float]]] = {}

    def _incr_window(self, key: str, window_sec: int) -> int:
        now = int(time.time())
        pipe = self.r.pipeline()
        member = f"{now}:{key}"
        pipe.zadd(key, {member: now})
        pipe.zremrangebyscore(key, 0, now - window_sec)
        pipe.zcard(key)
        _, _, count = pipe.execute()
        return int(count or 0)

    def velocity_features(self, customer_id: str) -> dict[str, float]:
        try:
            c1 = self._incr_window(f"vel:1m:{customer_id}", 60)
            c5 = self._incr_window(f"vel:5m:{customer_id}", 300)
            c60 = self._incr_window(f"vel:60m:{customer_id}", 3600)
        except redis.RedisError as exc:
            logger.error("redis velocity failed: %s", exc)
            c1 = c5 = c60 = -1.0
        return {"v_tx_1m": float(c1), "v_tx_5m": float(c5), "v_tx_1h": float(c60)}

    def _rolling_amount_stats(self, customer_id: str, amount: float) -> tuple[float, float]:
        q = self._local_rollups.setdefault(customer_id, deque(maxlen=200))
        q.append((time.time(), amount))
        if not q:
            return amount, 0.0
        amounts = [a for _, a in q]
        mu = float(np.mean(amounts))
        sigma = float(np.std(amounts)) or 1e-6
        return mu, sigma

    def amount_deviation(self, customer_id: str, amount: float) -> float:
        mu, sigma = self._rolling_amount_stats(customer_id, amount)
        return float(abs(amount - mu) / sigma)

    def geolocation_anomaly(self, customer_id: str, lat: float, lon: float) -> float:
        try:
            prev = self.r.geopos(f"geo:{customer_id}", "last")
            self.r.geoadd(f"geo:{customer_id}", (lon, lat, "last"))
            if not prev or prev[0] is None:
                return 0.0
            plon, plat = prev[0]
            if plon is None or plat is None:
                return 0.0
            km = self._haversine_km(float(plat), float(plon), lat, lon)
            return float(min(1.0, km / 500.0))
        except redis.RedisError:
            return 0.0

    def device_match_score(self, customer_id: str, device_fp: str) -> float:
        h = hashlib.sha256(device_fp.encode()).hexdigest()[:16]
        key = f"dev:{customer_id}"
        try:
            known = self.r.sismember(key, h)
            self.r.sadd(key, h)
            self.r.expire(key, 86400 * 30)
            return 0.0 if known else 1.0
        except redis.RedisError:
            return 0.5

    def mcc_risk(self, mcc: str) -> float:
        return _MCC_RISK.get(mcc, 0.35)

    def _haversine_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        r = 6371.0
        p1, p2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dl = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
        return 2 * r * math.asin(min(1.0, math.sqrt(a)))

    def build(self, evt: TransactionEvent) -> dict[str, float]:
        feats = self.velocity_features(evt.customer_id)
        feats["amount_z"] = self.amount_deviation(evt.customer_id, evt.amount)
        feats["geo_score"] = self.geolocation_anomaly(evt.customer_id, evt.lat, evt.lon)
        feats["device_new"] = self.device_match_score(evt.customer_id, evt.device_fp)
        feats["mcc_risk"] = self.mcc_risk(evt.mcc)
        return feats
