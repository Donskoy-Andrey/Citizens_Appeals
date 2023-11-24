import re
import emoji
from datetime import date, timedelta

pattern_mail = re.compile(
    r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
)
pattern_link = re.compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)
pattern_number = re.compile(
    # r'\b(\+?[7,8]\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b'
    "(\\+?\\d{1,4}?[-.\\s]?\\(?\\d{2,3}?\\)?[-.\\s]?\\d{2,4}[-.\\s]?\\d{2,4}[-.\\s]?\\d{2,9})"
)
# "(\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9})"
pattern_digit = re.compile(r"\+?\d+")

pattern_data = re.compile(
    r"\b(\d{1,2}\W\d{1,2}\W\d{2}|\d{2}\W\d{1,2}\W\d{1,2}|\d{1,2}\W\d{1,2}\W\d{4}|\d{4}\W\d{1,2}\W\d{2})\b"
    # "/(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[ \/\.\-]/"
)


def preprocess_for_model(raw_str: str) -> str:
    """
    Preprocess  citizen's appeal for neural model

    Parameters
    ----------
    raw_str : str
        Citizen's appeal.
    """
    numbers = pattern_number.findall(raw_str)
    for num in numbers:
        num1 = pattern_digit.findall(num)
        num_concoction = "".join(num1)

        if num_concoction[0] == "+":
            if len(num_concoction[1:]) == 11:
                raw_str = raw_str.replace(num, "(номер телефона)")
        else:
            if len(num_concoction) == 11:
                raw_str = raw_str.replace(num, "(номер телефона)")

    links = pattern_link.findall(raw_text)
    for link in links:
        raw_str = raw_str.replace(link, "(ccылка)")

    mails = pattern_mail.findall(raw_text)
    for mail in mails:
        raw_str = raw_str.replace(mail, "(почта)")

    datas = pattern_data.findall(raw_text)
    for data in datas:
        raw_str = raw_str.replace(data, "(дата)")
    return raw_str


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
    if raw_text[0] == "'" or raw_text[0] == '"':
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


def string_validator(raw_text: str) -> (dict, str):
    """
    Validation string for output on the screen

    Parameters
    ----------
    raw_text : str
        Citizen's appeal.
    """
    valid_data = {
        "Номер": [],
        "Ссылки": [],
        "Почта": [],
        "Адрес:": [],
        "Дата": [],
    }

    if not isinstance(raw_text, str):
        return valid_data, raw_text

    if len(raw_text) <= 5:
        return valid_data, raw_text

    raw_text = replace_day(raw_text)

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

    return valid_data, raw_text


def replace_day(raw_text: str) -> str:
    """
    replacing text data with datatime

    Parameters
    ----------
    raw_text : str
        Citizen's appeal.
    """

    days = [
        "позавчера",
        "послезавтра",
        "вчера",
        "сегодня",
        "завтра",
    ]
    for day in days:
        if day == "послезавтра":
            raw_text = raw_text.replace(
                day, f"{date.today() + timedelta(days=2)}"
            )
        if day == "позавчера":
            raw_text = raw_text.replace(
                day, f"{date.today()- timedelta(days=2)}"
            )
        if day == "вчера":
            raw_text = raw_text.replace(
                day, f"{date.today() - timedelta(days=1)}"
            )
        if day == "сегодня":
            raw_text = raw_text.replace(day, f"{date.today()}")
        if day == "завтра":
            raw_text = raw_text.replace(
                day, f"{date.today() + timedelta(days=1)}"
            )
    return raw_text


if __name__ == "__main__":
    raw_text = "8(929) - 296 - 14 - 84"
    raw_text = preprocess_str(raw_text)
    res = string_validator(raw_text)
    preprocess_for_model(raw_text)
    # print(res)
