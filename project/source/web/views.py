import time

from django.shortcuts import render, redirect
from project.source.string_processing.utilities import highlight_words
from project.source.ml.inference import setup_model
from project.source.utils import theme_to_group
from project.source.web.models import Appeal

ml_model = setup_model()
theme_to_group_mapping = theme_to_group(processing=True)


def main_win(request):

    print(f"{request.POST=}")
    if "post_content" in request.POST:
        text = request.POST.get("post_content")
        print(f"{text=}")
        if text == "":
            return render(request, "main.html")
        else:
            text = highlight_words(text)
            executors, themes = ml_model.predict(text)
            print(f"{list(themes)=}")
            groups = [theme_to_group_mapping[theme] for theme in themes]
            print(
                f"Исполнитель: {executors}\n",
                f"Тема: {themes}\n",
                f"Группа тем: {groups}\n",
            )
            record = Appeal(
                text=text,
                executor=executors[0],
                theme=themes[0],
                group=groups[0],
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
                },
            )
    else:
        return render(request, "main.html")
