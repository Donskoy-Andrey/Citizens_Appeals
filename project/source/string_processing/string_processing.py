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

    valid_data = {"Номер": [], "Ссылки": [], "Почта": [], "Адрес:": []}

    numbers = pattern_number.findall(raw_text)
    for num in numbers:
        print(num)
        num1 = pattern_digit.findall(num)
        num_concoction = "".join(num1)
        if num_concoction[0] == "+":
            if len(num_concoction[1:]) == 11:
                valid_data["Номер"].append(num)
        else:
            if len(num_concoction) == 11:
                valid_data["Номер"].append(num)

    links = pattern_link.findall(raw_text)
    valid_data["Ссылки"].extend(links)

    mails = pattern_mail.findall(raw_text)
    valid_data["Почта"].extend(mails)

    return valid_data


string_processing(
    "ддддддывывы +79292961484 8 (963) 4051547 фыфыфы    asasasasa@gmail.com   asasas@gmail.com"
)
# print(valid_data)
