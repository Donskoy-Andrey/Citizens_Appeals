import spacy


nlp = spacy.load("ru_core_news_sm")


def trigger_word(text: str) -> list[str]:

    template_trigger_words = [
        "убийство",
        "смерть",
        "убийца",
        "терроризм",
        "террорист",
        "гибель",
        "теракт",
        "землетрясение",
        "пожар",
        "взрыв",
        "труп",
        "взрывное",
        "взрывчатое",
        "террористическая",
        "заложник",
        "бомба",
        "оружие",
        "грабитель",
        "изнасилование",
        "покушение",
        "убить",
        "преступление",
        "правонарушение",
    ]
    trigger_words = []
    try:
        doc = nlp(text)
        for token in doc:
            if token.lemma_ in template_trigger_words:
                trigger_words.append(token.text)
    finally:
        return trigger_words


if __name__ == "__main__":
    text = "Я  критический,грабители  смерти успокоилась. Вы меня извините, 3600 и 5600. Вы что не понимаете, он ещё ничего не видел. С какой стати, с какой стати ааааааа."
    trigger_word(text)
