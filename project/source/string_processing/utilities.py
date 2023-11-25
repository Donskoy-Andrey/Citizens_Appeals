import re
import time

from project.source.ml.entity import predict_entity
from project.source.ml.trigger_word import trigger_word
from project.source.string_processing.validator_string import (
    preprocess_str,
    string_validator,
    preprocess_for_model,
)


def find_start_end(string, pattern):
    """
    Finds start and end indexes of pattern in string(for highlighting).
    :param string:
    :param pattern:
    :return:
    """
    for elem in r"\.^$*+?{}[]|()":
        pattern = pattern.replace(f"{elem}", rf"\{elem}")
    matches = re.finditer(pattern, string)
    start_end_list = []
    for match in matches:
        start_end_list.append((match.start(), match.end()))
    return start_end_list


def highlight_words(text: str) -> str:
    """
    Creates html block with highlighted objects;
    :param text:
    :return:
    """
    try:
        to_highlight, new_text = string_validator(text)
        text_for_model = preprocess_for_model(text)
        to_highlight_additional = predict_entity(text_for_model)

        end_tag = "</u></a>"
        for key, value in dict(to_highlight, **to_highlight_additional).items():
            if key == "Номер":
                tag = '<a class="highlighted_text phone_number"><u><span class="tooltip-text phone_number" id="top">Номер</span> '
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
                if len(word) < 2:
                    continue
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
    except Exception:
        print("###_Exception in callback_###")
        return text
    else:
        print("###_Text_generated successfully_###")
        return new_text
    finally:
        pass


def highlight_trigger(text: str, clear_text: str) -> (str, bool):
    tag = '<a class="highlighted_text trigger_word"><u><span class="tooltip-text trigger_word" id="top">Триггер</span> '
    end_tag = "</u></a>"
    trigger_words = trigger_word(clear_text)
    if len(trigger_words) == 0:
        return text, False
    new_text = text
    for word in trigger_words:
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

    return new_text, True


if __name__ == "__main__":
    text = (
        "ддддддывывыфыфыфы  89164444444  asasasasa@gmail.com   asasas@gmail.com"
    )
    print(highlight_words(text))
