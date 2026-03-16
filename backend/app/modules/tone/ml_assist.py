import joblib
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "phishing_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

_model = joblib.load(MODEL_PATH)
_vectorizer = joblib.load(VECTORIZER_PATH)

def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\W+", " ", text)
    return text.strip()


def get_ml_probability(text: str) -> float:
    """
    Returns probability that text is phishing/spam.
    ML is advisory only.
    """
    cleaned = _clean_text(text)
    vec = _vectorizer.transform([cleaned])
    prob = _model.predict_proba(vec)[0][1]
    return float(prob)
