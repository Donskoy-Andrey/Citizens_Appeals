import pandas as pd
import emoji
import re


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
