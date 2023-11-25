from transformers import pipeline

pipe = pipeline(
    "token-classification",
    model="viktoroo/sberbank-rubert-base-collection3",
    aggregation_strategy="simple",
)


def predict_entity(text: str):
    """
    Highlights entities such as date, organization, location in text.
    :param text:
    :return res | text:
    """
    try:
        word_descriptions = pipe.predict(text)
        res = {
            "location": [],
            "person": [],
            "organization": [],
        }
        for word_description in word_descriptions:
            group = word_description["entity_group"]
            # word_start = word_description["start"]
            # word_end = word_description["end"]
            word = word_description["word"]

            if group == "LOC":
                res["location"].append(word)
                pass
            if group == "PER":
                res["person"].append(word)
                pass
            if group == "ORG":
                res["organization"].append(word)
                pass
    except Exception:
        print("###_Exception in entity prediction_###")
        return {
            "location": [],
            "person": [],
            "organization": [],
        }
    else:
        return res
