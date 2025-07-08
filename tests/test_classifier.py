from app.services.classifier import classify
from app.models.email import EmailIn

def test_spam():
    email = EmailIn(subject="Win", body="You won a million dollars")
    out   = classify(email)
    assert out.label in {"spam", "phishing", "authentic"}
