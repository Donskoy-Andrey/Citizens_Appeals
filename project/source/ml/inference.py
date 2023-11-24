import torch
import pickle
from transformers import AutoModel, AutoTokenizer, AutoConfig
from project.source.config import (
    LANGUAGE_MODEL_NAME,
    EXECUTOR_ENCODER_PATH,
    THEME_ENCODER_PATH,
    DEVICE,
    MODEL_PATH,
)
from project.source.ml.classifier import Classifier


def setup_model():
    """
    Main function for setup model.

    Returns
    -------
    Model instance
    """

    with open(EXECUTOR_ENCODER_PATH, "rb") as file:
        executor_encoder = pickle.load(file)

    with open(THEME_ENCODER_PATH, "rb") as file:
        theme_encoder = pickle.load(file)

    language_model = AutoModel.from_config(
        AutoConfig.from_pretrained(LANGUAGE_MODEL_NAME)
    )
    tokenizer = AutoTokenizer.from_pretrained(
        LANGUAGE_MODEL_NAME, model_max_length=512
    )
    classifier = Classifier(
        language_model, tokenizer, executor_encoder, theme_encoder, hid_size=768
    ).to(DEVICE)
    classifier.load_state_dict(
        torch.load(MODEL_PATH, map_location=torch.device(DEVICE))
    )
    return classifier


if __name__ == "__main__":
    model = setup_model()
    output = model.predict(["Обколоться бы вакциной"])
    print(output)
