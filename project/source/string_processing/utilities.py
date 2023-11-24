import re
import time

from project.source.string_processing.validator_string import string_validator


def find_start_end(string, pattern):
    matches = re.finditer(pattern, string)
    start_end_list = []
    for match in matches:
        start_end_list.append((match.start(), match.end()))
    return start_end_list


def highlight_words(text):
    to_highlight = string_validator(text)
    new_text = text
    end_tag = "</u></a>"

    for key, value in to_highlight.items():
        if key == "Номер":
            tag = '<a class="highlighted_text phone_number"><u>'
        elif key == "Ссылки":
            tag = '<a class="highlighted_text link"><u>'
        elif key == "Почта":
            tag = '<a class="highlighted_text email"><u>'
        else:
            tag = '<a class="highlighted_text date_time"><u>'
        for word in value:

            print(f"{new_text=} {word=}")
            positions = find_start_end(new_text, word)
            print(f"{positions}")
            for i in range(len(positions)):
                pos = find_start_end(new_text, word)
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
