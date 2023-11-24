import re
import time

from project.source.ml.entity import predict_entity
from project.source.string_processing.validator_string import (
    preprocess_str,
    string_validator,
)


def find_start_end(string, pattern):
    matches = re.finditer(pattern, string)
    start_end_list = []
    for match in matches:
        start_end_list.append((match.start(), match.end()))
    return start_end_list


def highlight_words(text):
    print(f"{string_validator(text)=}")
    to_highlight, new_text = string_validator(text)
    to_highlight_additional = predict_entity(new_text)

    end_tag = "</u></a>"

    for key, value in dict(to_highlight, **to_highlight_additional).items():
        if key == "Номер":
            tag = '<a class="highlighted_text phone_number"><u><span class="tooltip-text phone_number" id="top">Номер</span>'
        elif key == "Ссылки":
            tag = '<a class="highlighted_text link"><u><span class="tooltip-text link" id="top">Ссылка</span>'
        elif key == "Почта":
            tag = '<a class="highlighted_text email"><u><span class="tooltip-text email" id="top">Почта</span>'
        elif key == "Дата":
            tag = '<a class="highlighted_text date_time"><u><span class="tooltip-text date_time" id="top">Дата</span>'
        elif key == "location":
            tag = '<a class="highlighted_text location"><u><span class="tooltip-text location" id="top">Местоположение</span>'
        elif key == "person":
            tag = '<a class="highlighted_text person"><u><span class="tooltip-text person" id="top">ФИО</span>'
        elif key == "organization":
            tag = '<a class="highlighted_text organization"><u><span class="tooltip-text organization" id="top">Организация</span>'
        for word in value:
            positions = find_start_end(new_text.lower(), word.lower())
            for i in range(len(positions)):
                pos = find_start_end(new_text.lower(), word.lower())
                new_text = (
                    new_text[: pos[i][0]]
                    + tag
                    + new_text[pos[i][0] : pos[i][1]]
                    + end_tag
                    + new_text[pos[i][1] :]
                )

    return new_text


if __name__ == "__main__":
    text = (
        "ддддддывывыфыфыфы  89164444444  asasasasa@gmail.com   asasas@gmail.com"
    )
    print(highlight_words(text))
