"""Sentiment analysis using Hugging Face Transformers."""
from transformers import pipeline

_sentiment_pipeline = None

def _get_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True,
            max_length=512,
        )
    return _sentiment_pipeline

def score_text(text):
    """
    Analyze sentiment of text using a pre-trained model.
    Returns (label, score) where label is POSITIVE/NEGATIVE and score is float.
    Score is polarity: positive values for POSITIVE, negative for NEGATIVE.
    """
    if not text or not text.strip():
        return "NEUTRAL", 0.0
    pipe = _get_pipeline()
    result = pipe(text[:512])[0]  
    label = result["label"]
    confidence = float(result["score"])
    score = confidence if label == "POSITIVE" else -confidence
    return label, score
