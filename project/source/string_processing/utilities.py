import re
import time

from project.source.string_processing.validator_string import (
    preprocess_str,
    string_validator,
)


def find_start_end(string, pattern):
    print(f"{string=} {pattern}")
    matches = re.finditer(pattern, string)
    start_end_list = []
    for match in matches:
        start_end_list.append((match.start(), match.end()))
    return start_end_list


def highlight_words(text: str) -> str:
    to_highlight, new_text = string_validator(preprocess_str(text))
    end_tag = "</u></a>"
    for key, value in to_highlight.items():
        if key == "Номер":
            tag = '<a style="background:green"><u>'
        elif key == "Ссылки":
            tag = '<a style="background:yellow"><u>'
        elif key == "Почта":
            tag = '<a style="background:red"><u>'
        else:
            tag = '<a style="background:white"><u>'
        for word in value:

            positions = find_start_end(new_text, word)
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
