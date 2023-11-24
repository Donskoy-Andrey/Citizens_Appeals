import pandas as pd

# Dataset
DATASET_PATH = "data/raw/train_dataset_train.csv"
DATA = pd.read_csv(DATASET_PATH, sep=";")

# Model
DEVICE = "cpu"
LANGUAGE_MODEL_NAME = "DeepPavlov/distilrubert-base-cased-conversational"
MODEL_PATH = "models/distilbert.pt"
THEME_ENCODER_PATH = "models/theme_encoder.obj"
EXECUTOR_ENCODER_PATH = "models/executor_encoder.obj"
