import re
import emoji

pattern_mail = re.compile(
    r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
)
pattern_link = re.compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)
pattern_number = re.compile(
    "\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}"
)
pattern_digit = re.compile(r"\+?\d+")

pattern_data = re.compile(
    r"\b(\d{1,2}\W\d{1,2}\W\d{2,4}|\d{2,4}\W\d{1,2}\W\d{1,2})\b"
)


def preprocess_str(raw_str: str, demojize: bool = True) -> str:
    """
    Preliminary processing of a citizen’s appeal

    Parameters
    ----------
    raw_str : str
        Citizen's appeal.
    demojize : bool
        Convert emojis to plain text (takes time!)
    """

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


def string_validator(raw_text: str) -> dict | int:
    """
    Input string validation

    Parameters
    ----------
    raw_text : str
        Citizen's appeal.
    """

    if not isinstance(raw_text, str):
        return 0  # неверный формат данных

    if len(raw_text) <= 5:
        return 1  # некорректная строка

    raw_text = preprocess_str(raw_text)

    valid_data = {
        "Номер": [],
        "Ссылки": [],
        "Почта": [],
        "Адрес:": [],
        "Дата": [],
    }

    numbers = pattern_number.findall(raw_text)
    for num in numbers:
        num1 = pattern_digit.findall(num)
        num_concoction = "".join(num1)

        if num_concoction[0] == "+":
            if len(num_concoction[1:]) == 11:
                valid_data["Номер"].append(num)
        else:
            if len(num_concoction) == 11:
                valid_data["Номер"].append(num)

    links = pattern_link.findall(raw_text)
    valid_data["Ссылки"].extend(set(links))

    mails = pattern_mail.findall(raw_text)
    valid_data["Почта"].extend(set(mails))

    datas = pattern_data.findall(raw_text)
    valid_data["Дата"].extend(set(datas))

    return valid_data


if __name__ == "__main__":
    raw_text = "Пермь"
    raw_text = preprocess_str(raw_text)
    res = string_validator(raw_text)
    print(res)
