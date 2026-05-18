import pytest
from src.model import FraudDetectionModel

# tests for the fraud detection model
def test_model_initialization():
    model = FraudDetectionModel()
    assert model is not None
    assert model.threshold == 0.5  # default threshold

def test_model_prediction():
    model = FraudDetectionModel()
    sample_data = {
        'transaction_amount': 1500,
        'user_id': 'user_123',
        'location': 'online',
        'merchant_id': 'merchant_456',
    }
    prediction = model.predict(sample_data)
    assert prediction in [0, 1]  # expects binary output

def test_model_high_risk_prediction():
    model = FraudDetectionModel()
    high_risk_data = {
        'transaction_amount': 5000,
        'user_id': 'user_789',
        'location': 'international',
        'merchant_id': 'merchant_987',
    }
    prediction = model.predict(high_risk_data)
    assert prediction == 1  # should flag as fraud

def test_model_low_risk_prediction():
    model = FraudDetectionModel()
    low_risk_data = {
        'transaction_amount': 100,
        'user_id': 'user_001',
        'location': 'local',
        'merchant_id': 'merchant_002',
    }
    prediction = model.predict(low_risk_data)
    assert prediction == 0  # should not flag as fraud

# TODO: add more edge cases for predictions