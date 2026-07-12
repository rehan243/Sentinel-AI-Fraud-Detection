"""fraud scoring stack — features, API, alerts. not legal advice."""

from src.feature_engine import FeatureEngine, TransactionEvent
from src.model_server import create_app
from src.alert_pipeline import AlertPipeline, AlertDecision, RoutingOutcome

__all__ = [
    "FeatureEngine",
    "TransactionEvent",
    "create_app",
    "AlertPipeline",
    "AlertDecision",
    "RoutingOutcome",
]

def initialize_feature_engine() -> FeatureEngine:
    """initialize feature engine with error handling"""
    try:
        engine = FeatureEngine()
    except Exception as e:
        print(f"error initializing feature engine: {e}")
        raise
    return engine

def setup_alert_pipeline() -> AlertPipeline:
    """setup alert pipeline with error handling"""
    try:
        pipeline = AlertPipeline()
    except Exception as e:
        print(f"error setting up alert pipeline: {e}")
        raise
    return pipeline

# TODO: consider adding more detailed logging for debugging
# also, maybe include specific exception types to catch
# might want to add a test for error scenarios in the future