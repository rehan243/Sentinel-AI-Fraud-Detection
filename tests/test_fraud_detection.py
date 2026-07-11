import pytest
from fraud_detection import FraudDetector  # assuming this is where the logic is

def test_fraud_detection_high_risk():
    # tests a high-risk case
    detector = FraudDetector()
    transaction = {
        'amount': 10000,
        'location': 'offshore',
        'transaction_type': 'wire_transfer'
    }
    assert detector.is_fraudulent(transaction) is True

def test_fraud_detection_low_risk():
    # tests a low-risk case
    detector = FraudDetector()
    transaction = {
        'amount': 100,
        'location': 'local',
        'transaction_type': 'deposit'
    }
    assert detector.is_fraudulent(transaction) is False

def test_fraud_detection_edge_case():
    # tests an edge case with amount exactly on the threshold
    detector = FraudDetector()
    transaction = {
        'amount': 5000,
        'location': 'local',
        'transaction_type': 'withdrawal'
    }
    assert detector.is_fraudulent(transaction) is False  # assuming threshold is above this

def test_fraud_detection_invalid_transaction():
    # tests invalid transaction input
    detector = FraudDetector()
    transaction = {
        'amount': -100,
        'location': 'unknown',
        'transaction_type': 'unknown'
    }
    with pytest.raises(ValueError):
        detector.is_fraudulent(transaction)

# TODO: add more tests for different scenarios