import time

from django.shortcuts import render, redirect
from project.source.string_processing.utilities import highlight_words
from project.source.ml.inference import setup_model
from project.source.ml.sentiment import predict_sentiment
from project.source.utils import theme_to_group
from project.source.web.models import Appeal

ml_model = setup_model()
theme_to_group_mapping = theme_to_group(processing=True)


def main_win(request):
    if "post_content" in request.POST:
        text = request.POST.get("post_content")
        if text == "":
            return render(request, "main.html")
        else:
            sentiment = predict_sentiment(text)
            sentiment_cases = {
                "negative": "negative",
                "positive": "positive",
                "neutral": "neutral",
            }
            sentiment_addition = sentiment_cases.get(sentiment)
            if not sentiment_addition:
                sentiment_addition = ""
            text = highlight_words(text)
            executors, themes = ml_model.predict(text)
            groups = [theme_to_group_mapping[theme] for theme in themes]
            record = Appeal(
                text=text,
                executor=executors[0],
                theme=themes[0],
                group=groups[0],
                sentiment=sentiment_addition,
            )
            record.save()

            return render(
                request,
                "main.html",
                {
                    "text": text,
                    "executor": executors[0],
                    "theme": themes[0],
                    "group": groups[0],
                    "sentiment": sentiment_addition,
                },
            )
    else:
        return render(request, "main.html")
