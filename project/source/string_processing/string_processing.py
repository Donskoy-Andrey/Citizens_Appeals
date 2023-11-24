import re


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


def string_processing(raw_text: str) -> dict:
    valid_data = {"Номер": [], "Ссылки": [], "Почта": []}
    numbers = pattern_number.findall(raw_text)
    for num in numbers:
        n = pattern_digit.findall(num)
        n = "".join(n)
        if n[0] == "+":
            if len(n[1:]) == 11:
                valid_data["Номер"].append(n)
        else:
            if len(n) == 11:
                valid_data["Номер"].append(n)

    links = pattern_link.findall(raw_text)
    valid_data["Ссылки"].extend(links)

    mails = pattern_mail.findall(raw_text)
    valid_data["Почта"].extend(mails)
    return valid_data


string_processing(
    "ддддддывывы+7 (929) 296 14 84 8 (963) 405 15 47фыфыфы    asasasasa@gmail.com   asasas@gmail.com"
)
# print(valid_data)
