import time

from django.shortcuts import render, redirect
from project.source.string_processing.utilities import highlight_words


def main_win(request):
    print(f"{request.POST=}")
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
