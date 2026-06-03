import pytest
from fraud_detection.rules import apply_fraud_rules
from fraud_detection.scoring import calculate_risk_score

# test cases for rule application
def test_apply_fraud_rules():
    input_data = {
        'transaction_amount': 1500,
        'user_location': 'high_risk_area',
        'transaction_type': 'cash'
    }
    
    result = apply_fraud_rules(input_data)
    # expect the rule to flag this as fraudulent
    assert result is True

    input_data['transaction_amount'] = 100
    input_data['user_location'] = 'low_risk_area'
    
    result = apply_fraud_rules(input_data)
    # expect this to not be flagged as fraudulent
    assert result is False

# test cases for risk scoring
def test_calculate_risk_score():
    input_data = {
        'transaction_history': [100, 200, 300],
        'user_age': 30,
        'account_age': 5
    }
    
    score = calculate_risk_score(input_data)
    # let's say we have a simple scoring logic where lower is better
    assert score >= 0 and score <= 100

    input_data['transaction_history'] = [1000, 2000, 3000]
    
    score = calculate_risk_score(input_data)
    # higher transaction amounts should increase risk score
    assert score > 50  # TODO: adjust based on actual scoring logic

# run tests
if __name__ == "__main__":
    pytest.main()