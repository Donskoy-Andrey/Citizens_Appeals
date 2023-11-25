import pandas as pd
import emoji
import re


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
    r"\b(\d{1,2}\W\d{1,2}\W\d{2,4}|\d{2,4}\W\d{1,2}\W\d{1,2})\b"
    # "/(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[ \/\.\-]/"
)


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
    # processed_data["Тема"] = processed_data["Тема"].apply(lambda x : x[2:] if x[:2] == "★ " else x)

    # Demojinize.
    if demojize:
        processed_data["Текст инцидента"] = processed_data[
            "Текст инцидента"
        ].apply(emoji.demojize)

    # Parse VK replies.
    pattern_VK = re.compile(r"\[(?P<ID>\w+)\|(?P<NAME>[^\[^\]]*)\]")
    processed_data["Текст инцидента"] = processed_data["Текст инцидента"].apply(
        lambda x: pattern_VK.sub("\g<NAME>", x)
    )

    # Replace whitespace expressions.
    whitespace_substrings = {"<br>", "\\n"}
    pattern_whitespace = re.compile(
        "|".join(re.escape(substring) for substring in whitespace_substrings)
    )
    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(pattern_whitespace, " ", regex=True)
    # for substring in whitespace_substrings:
    #    processed_data["Текст инцидента"].str.replace(substring, " ")

    # Replace multiple whitespaces with one.
    pattern_multiple_whitespace = re.compile("\s+")
    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(pattern_multiple_whitespace, " ", regex=True)

    # Remove numbers, mails, links, dates...
    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(pattern_mail, "(почта)", regex=True)

    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(pattern_link, "(ccылка)", regex=True)

    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(pattern_data, "(дата)", regex=True)

    processed_data["Текст инцидента"] = processed_data[
        "Текст инцидента"
    ].str.replace(pattern_number, "(номер)", regex=True)

    return processed_data


def theme_to_group(data) -> dict:
    """
    Mapping for theme to group

    Parameters
    ----------
    data: pd.DataFrame
        Data

    Returns
    -------
        Mapping
    """

    mapping = (
        data[["Тема", "Группа тем"]]
        .drop_duplicates()
        .set_index("Тема")
        .to_dict()["Группа тем"]
    )

    return mapping
