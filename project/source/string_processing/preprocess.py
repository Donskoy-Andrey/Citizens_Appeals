import re

import emoji
import pandas as pd


def preprocess_str(raw_str: str, demojize: bool = True) -> str:
    raw_text = raw_str
    raw_text = raw_text[1:]
    if demojize:
        raw_text = emoji.demojize(raw_text, "")

    VK_regexp = re.compile(r"\[(?P<ID>\w+)\|(?P<NAME>[^\[^\]]*)\]")
    raw_text = VK_regexp.sub("\g<NAME>", raw_text)

    whitespace_substrings = {"<br>", "\\n"}
    whitespace_regexp = re.compile(
        "|".join(re.escape(substring) for substring in whitespace_substrings)
    )
    raw_text = re.sub(whitespace_regexp, " ", raw_text)

    ultiple_whitespace_regexp = re.compile("\s+")
    raw_text = re.sub(ultiple_whitespace_regexp, " ", raw_text)
    return raw_text


def preprocess_data(data: pd.DataFrame, demojize: bool = True) -> pd.DataFrame:
    """
    Preprocess the data

    Parameters
    ----------
    data : pd.DataFrame
        Input data to preprocess.
    demojize : bool
        Convert emojis to plain text (takes time!)
    """

    processed_data = data.copy()

    # Delete "'" at the start of the line.
    # data["Текст инцидента"].apply(lambda x : x[1:] if x[0] == "'" else x)
    processed_data["Текст инцидента"] = processed_data["Текст инцидента"].apply(
        lambda x: x[1:]
    )

    # Delete "*" from themes names.
    processed_data["Тема"] = processed_data["Тема"].apply(
        lambda x: x[2:] if x[:2] == "★ " else x
    )

    # Demojinize.
    if demojize:
        processed_data["Текст инцидента"] = processed_data[
            "Текст инцидента"
        ].apply(emoji.demojize)

    # Parse VK replies.
    VK_regexp = re.compile(r"\[(?P<ID>\w+)\|(?P<NAME>[^\[^\]]*)\]")
    # matches = VK_regexp.finditer(line)
    processed_data["Текст инцидента"] = processed_data["Текст инцидента"].apply(
        lambda x: VK_regexp.sub("\g<NAME>", x)
    )

    # Replace whitespace expressions.
    whitespace_substrings = {"<br>", "\\n"}
    whitespace_regexp = re.compile(
        "|".join(re.escape(substring) for substring in whitespace_substrings)
    )
    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(whitespace_regexp, " ", regex=True)
    # for substring in whitespace_substrings:
    #    processed_data["Текст инцидента"].str.replace(substring, " ")

    # Replace multiple whitespaces with one.
    multiple_whitespace_regexp = re.compile("\s+")
    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(multiple_whitespace_regexp, " ", regex=True)

    return processed_data


sss = "'Добрый день!<br>Помогите связаться с пресс-службой, пожалуйста. Второй день не могу дозвониться по телефону, указанном на сайте, - 235-15-60.<br>Отправила запрос на съемку на общий адрес (info@minzdrav.permkrai.ru), но не знаю, получили ли его в пресс-службе и можно ли ожидать скорого рассмотрения.<br>С уважением,<br>Дарья Вахрушева<br>продюсер программы 'Герои'<br>+79221395668"
preprocess_str(sss)
