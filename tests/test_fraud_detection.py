import pytest
from fraud_detection import FraudDetector  # assuming this is the main class for detection

def test_high_risk_score():
    detector = FraudDetector()
    transaction = {"amount": 1000, "location": "suspicious_area", "is_new_account": True}
    score = detector.calculate_risk_score(transaction)
    
    # checking if the score is above a certain threshold for high-risk
    assert score > 75, f"expected a high risk score but got {score}"

def test_low_risk_score():
    detector = FraudDetector()
    transaction = {"amount": 50, "location": "safe_area", "is_new_account": False}
    score = detector.calculate_risk_score(transaction)
    
    # checking if the score is below a certain threshold for low-risk
    assert score < 25, f"expected a low risk score but got {score}"

def test_score_for_existing_customer():
    detector = FraudDetector()
    transaction = {"amount": 500, "location": "safe_area", "is_new_account": False}
    score = detector.calculate_risk_score(transaction)
    
    # existing customers typically should not be high risk
    assert score < 50, f"expected a reasonable score for existing customer but got {score}"

def test_score_for_large_amount():
    detector = FraudDetector()
    transaction = {"amount": 5000, "location": "unknown_area", "is_new_account": True}
    score = detector.calculate_risk_score(transaction)
    
    # large amounts should raise the risk score
    assert score >= 60, f"expected a higher score for large amounts but got {score}"

# TODO: add more tests to cover edge cases and variations