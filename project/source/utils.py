import pandas as pd
from project.source.config import DATA
from project.source.ml.preprocess import preprocess_data


def theme_to_group(processing: bool = False) -> pd.DataFrame:
    """
    Mapping for theme to group

    Parameters
    ----------
    processing: bool
        use processing or not

    Returns
    -------
        Mapping
    """

    if processing:
        df = preprocess_data(DATA)
    else:
        df = DATA

    mapping = (
        df[["Тема", "Группа тем"]]
        .drop_duplicates()
        .set_index("Тема")
        .to_dict()["Группа тем"]
    )

    return mapping


def group_to_theme(processing: bool = False) -> pd.DataFrame:
    """
    Mapping for group to theme

    Parameters
    ----------
    processing : bool
        use processing or not

    Returns
    -------
        Mapping
    """

    if processing:
        df = preprocess_data(DATA)
    else:
        df = DATA

    mapping = (
        df[["Тема", "Группа тем"]]
        .drop_duplicates()
        .set_index("Группа тем")
        .to_dict()["Тема"]
    )
    return mapping
