import time

from django.shortcuts import render, redirect
from project.source.string_processing.utilities import highlight_words
from project.source.ml.inference import setup_model
from project.source.utils import theme_to_group

# ml_model = setup_model()


def main_win(request):
    # executors, themes = ml_model.predict(
    #     ["Как же я обожаю вакцины", "Камазы, бетон и дороги очень сложно ехать"]
    # )
    # theme_to_group_mapping = theme_to_group(processing=True)
    #
    # groups = [theme_to_group_mapping[theme] for theme in themes]
    # print(
    #     f"Исполнитель: {executors}\n",
    #     f"Тема: {themes}\n",
    #     f"Группа тем: {groups}\n",
    # )
    # print(f"{request.POST=}")
    if "post_content" in request.POST:
        text = request.POST.get("post_content")
        print(f"{text=}")
        if text == "":
            return render(request, "main.html")
        else:
            text = highlight_words(text)
            return render(request, "main.html", {"text": text})
    else:
        return render(request, "main.html")
