def detect_intent(text):
    t = text.lower()

    if "transfer" in t or "send" in t:
        return "transfer"
    if "balance" in t:
        return "balance"
    if "saving" in t:
        return "saving"
    if "card" in t:
        return "card"

    return "unknown"
