import time

from django.shortcuts import render, redirect
from project.source.string_processing.utilities import highlight_words
from project.source.ml.inference import setup_model
from project.source.ml.sentiment import predict_sentiment
from project.source.ml.summary import summarize
from project.source.utils import theme_to_group
from project.source.web.models import Appeal
import pandas as pd
from plotly.offline import plot
from project.source.string_processing.validator_string import (
    preprocess_str,
    string_validator,
)
import plotly.express as px

from django.utils import timezone
from project.source.web.graph_plotter import plot_hist, plot_time_series

ml_model = setup_model()
theme_to_group_mapping = theme_to_group(processing=True)


def main_win(request):

    if "post_content" in request.POST:
        text = request.POST.get("post_content")
        if text == "":
            return render(request, "main.html")
        else:
            # _summary = summarize(text)
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
            executors, themes = ml_model.predict(preprocess_str(text))

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
                    # "summary": _summary,
                },
            )
    else:
        return render(request, "main.html")


def dashboard(request):
    print(f"{request.POST=}")

    qs = Appeal.objects.all()
    projects_data = [
        {
            "Исполнитель": x.executor,
            "Тема": x.theme,
            "Группа тем": x.group,
            "Дата": x.date,
        }
        for x in qs
    ]

    df = pd.DataFrame(projects_data)
    selected = "Исполнитель"
    if "selected_option" in request.POST:
        selected = request.POST.get("selected_option")
        fig = plot_hist(df, selected)
        time_series = plot_time_series(df, selected)

    else:
        fig = plot_hist(df, "Исполнитель")
        time_series = plot_time_series(df, "Исполнитель")

    gantt_plot = plot(fig, output_type="div")
    time_series_plot = plot(time_series, output_type="div")
    context = {
        "plot_div": gantt_plot,
        "time_series": time_series_plot,
        "selected": selected,
    }

    return render(request, "dashboard.html", context)
