import pytest
from fraud_detection import FraudDetector  # assuming this is the fraud detection class

# testing the fraud detection behavior
def test_fraud_detection_with_high_risk_score():
    detector = FraudDetector()
    input_data = {'transaction_amount': 1500, 'user_history': 'high_risk', 'location': 'suspicious_area'}
    result = detector.detect(input_data)
    assert result == True  # expect a fraud alert

def test_fraud_detection_with_low_risk_score():
    detector = FraudDetector()
    input_data = {'transaction_amount': 100, 'user_history': 'low_risk', 'location': 'normal_area'}
    result = detector.detect(input_data)
    assert result == False  # expect no fraud alert

def test_fraud_detection_edge_case():
    detector = FraudDetector()
    input_data = {'transaction_amount': 0, 'user_history': 'unknown', 'location': 'normal_area'}
    result = detector.detect(input_data)
    assert result == False  # check how it handles zero amount

# TODO: add more tests for different edge cases and types of transactions
def test_fraud_detection_with_missing_fields():
    detector = FraudDetector()
    input_data = {'transaction_amount': 500}  # missing user_history and location
    with pytest.raises(KeyError):
        detector.detect(input_data)  # expect an error for missing fields