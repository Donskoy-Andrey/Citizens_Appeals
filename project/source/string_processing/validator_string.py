import re

from preprocess import preprocess_str

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


def string_validator(raw_text: str) -> dict:

    valid_data = {"Номер": [], "Ссылки": [], "Почта": [], "Адрес:": []}

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
    valid_data["Ссылки"].extend(links)

    mails = pattern_mail.findall(raw_text)
    valid_data["Почта"].extend(mails)
    return valid_data


# raw_text = "Пермь г, +79194692145. В Перми с ноября 2021 года не работает социальное такси. Каким образом можно получить льготу по проезду в такси в https://m.vk.com/@valekse59-rss-2128466888-976298670<br>VK соц учреждения инвалиду 2гр.пррезд в общественном транспорте не возможен. Да и проездного льготного не представляется'Добрый день ! Скажите пожалуйста если подовала на пособие с 3 до 7 2 декабря , когда можно повторно подать ? вроде за 30 дней можно"
#
# string_validator(preprocess_str(raw_text))
