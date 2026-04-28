"""Rules + model score — sends Kafka messages so someone else owns delivery guarantees."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional

from kafka import KafkaProducer

logger = logging.getLogger(__name__)


class RoutingOutcome(str, Enum):
    AUTO_BLOCK = "auto_block"
    MANUAL_REVIEW = "manual_review"
    PASS = "pass"


@dataclass
class AlertDecision:
    outcome: RoutingOutcome
    priority: int
    score: float
    reasons: list[str]


class AlertPipeline:
    """Decision engine — inject producer for unit tests."""

    def __init__(
        self,
        kafka_brokers: list[str],
        topic: str = "fraud.alerts",
        producer: Optional[KafkaProducer] = None,
        customer_context_fn: Optional[Callable[[str], dict[str, Any]]] = None,
        dead_letter_topic: Optional[str] = None,
    ) -> None:
        self.topic = topic
        self._dead_letter = dead_letter_topic
        self._producer = producer or KafkaProducer(
            bootstrap_servers=kafka_brokers,
            value_serializer=lambda v: json.dumps(v).encode(),
            linger_ms=5,
        )
        self._ctx = customer_context_fn or (lambda cid: {"tier": "standard"})

    def _publish_raw(self, topic: str, key: Optional[bytes], msg: dict[str, Any]) -> None:
        self._producer.send(topic, key=key, value=msg)
        self._producer.flush(timeout=5)

    def _rules(
        self,
        score: float,
        velocity_1m: float,
        amount: float,
    ) -> list[str]:
        reasons: list[str] = []
        if score >= 0.92:
            reasons.append("model_high_risk")
        if velocity_1m >= 5:
            reasons.append("velocity_burst")
        if amount >= 5000:
            reasons.append("amount_threshold")
        return reasons

    def decide(
        self,
        txn_id: str,
        customer_id: str,
        model_score: float,
        features: dict[str, float],
        amount: float,
    ) -> AlertDecision:
        reasons = self._rules(model_score, features.get("v_tx_1m", 0.0), amount)
        ctx = self._ctx(customer_id)
        tier = ctx.get("tier", "standard")

        if "model_high_risk" in reasons and tier != "vip":
            outcome = RoutingOutcome.AUTO_BLOCK
            prio = 1
        elif reasons:
            outcome = RoutingOutcome.MANUAL_REVIEW
            prio = 5
        else:
            outcome = RoutingOutcome.PASS
            prio = 10

        return AlertDecision(outcome=outcome, priority=prio, score=model_score, reasons=reasons)

    def publish(self, decision: AlertDecision, payload: dict[str, Any]) -> None:
        msg = {
            "ts": time.time(),
            "outcome": decision.outcome.value,
            "priority": decision.priority,
            "score": decision.score,
            "reasons": decision.reasons,
            **payload,
        }
        key = (payload.get("customer_id") or "").encode() or None
        try:
            self._publish_raw(self.topic, key, msg)
        except Exception as exc:
            logger.error("kafka publish failed: %s", exc)
            if self._dead_letter:
                try:
                    self._publish_raw(self._dead_letter, key, {**msg, "error": str(exc)})
                except Exception as dlx:
                    logger.critical("dead letter also failed: %s", dlx)
            raise

    def dry_run(self, txn_id: str, customer_id: str, model_score: float, features: dict[str, float], amount: float) -> dict[str, Any]:
        """Same as decide + would-publish payload — for staging without Kafka."""
        d = self.decide(txn_id, customer_id, model_score, features, amount)
        return {
            "decision": d.outcome.value,
            "priority": d.priority,
            "reasons": d.reasons,
            "kafka_topic": self.topic,
        }
