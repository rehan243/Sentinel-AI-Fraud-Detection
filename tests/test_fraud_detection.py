import pytest
from src.fraud_detection import FraudDetector

def test_basic_fraud_detection():
    detector = FraudDetector()

    # test simple case where transaction amount is high
    transaction = {"amount": 1500, "location": "international", "user_id": 1}
    assert detector.is_fraudulent(transaction) == True

    # test case where transaction amount is low
    transaction = {"amount": 50, "location": "local", "user_id": 2}
    assert detector.is_fraudulent(transaction) == False

def test_location_based_fraud_detection():
    detector = FraudDetector()

    # high amount from a suspicious location
    transaction = {"amount": 2000, "location": "offshore", "user_id": 3}
    assert detector.is_fraudulent(transaction) == True

    # normal amount from a safe location
    transaction = {"amount": 100, "location": "local", "user_id": 4}
    assert detector.is_fraudulent(transaction) == False

def test_user_history_fraud_detection():
    detector = FraudDetector()

    # user with suspicious history
    transaction = {"amount": 500, "location": "local", "user_id": 5, "user_history": "suspicious"}
    assert detector.is_fraudulent(transaction) == True

    # user with clean history
    transaction = {"amount": 300, "location": "local", "user_id": 6, "user_history": "clean"}
    assert detector.is_fraudulent(transaction) == False

# TODO: add more tests for edge cases and different user profiles