from transformers import pipeline

sentiment_analysis = pipeline(
    "text-classification", model="cointegrated/rubert-tiny-sentiment-balanced"
)


def predict_sentiment(text: str):
    output = sentiment_analysis.predict(text)
    label = output[0]["label"]

    return label
