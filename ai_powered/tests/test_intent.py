from core.intent_classifier import classify_intent

def test_intent():
    assert classify_intent({"intent": "check_balance"}) == "check_balance"
