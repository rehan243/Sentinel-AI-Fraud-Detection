import pytest
from fraud_detection import FraudDetector  # assuming this is our main class

def test_fraud_detection_high_score():
    # testing high risk score
    detector = FraudDetector()
    score = detector.calculate_score(transaction_amount=10000, user_history='high-risk')
    assert score > 75, f"expected score to be greater than 75 but got {score}"

def test_fraud_detection_low_score():
    # testing low risk score
    detector = FraudDetector()
    score = detector.calculate_score(transaction_amount=100, user_history='low-risk')
    assert score < 25, f"expected score to be less than 25 but got {score}"

def test_fraud_detection_edge_case():
    # testing an edge case
    detector = FraudDetector()
    score = detector.calculate_score(transaction_amount=500, user_history='unknown')
    assert score == 50, f"expected score to be exactly 50 but got {score}"

def test_fraud_detection_invalid_input():
    # testing invalid input handling
    detector = FraudDetector()
    with pytest.raises(ValueError):
        detector.calculate_score(transaction_amount=-100, user_history='low-risk')

# TODO: add more tests for different user histories and transaction amounts