import random
import pandas as pd

DATASET_PATH = "data/raw/train_dataset_train.csv"


class TemplateModel:
    def __init__(self):
        self.model = "template model"
        self.themes = pd.read_csv(DATASET_PATH, sep=";")["Тема"].unique()

    def predict(self, string: str):
        print(f"Using {self.model} class for {string = }.")
        return random.choice(self.themes)
