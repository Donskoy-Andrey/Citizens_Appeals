import torch
import numpy as np
from sklearn.metrics import f1_score


class ClassifierHeads(torch.nn.Module):
    def __init__(
        self, executor_n_classes: int, theme_n_classes: int, hid_size: int
    ):
        super().__init__()

        self.linear_1 = torch.nn.Linear(hid_size, hid_size)
        self.executor_head = torch.nn.Linear(hid_size, executor_n_classes)
        self.theme_head = torch.nn.Linear(hid_size, theme_n_classes)

        self.dropout = torch.nn.Dropout(0.3)
        self.leaky_relu = torch.nn.LeakyReLU()
        self.log_soft_max = torch.nn.LogSoftmax(dim=1)

    def forward(self, embeddings):
        x = embeddings
        x = self.dropout(x)
        x = self.linear_1(x)
        x = self.dropout(x)
        x = self.leaky_relu(x)

        executor_logits = self.executor_head(x)
        theme_logits = self.theme_head(x)

        return self.log_soft_max(executor_logits), self.log_soft_max(
            theme_logits
        )


class Classifier(torch.nn.Module):
    def __init__(
        self,
        language_model,
        tokenizer,
        executor_encoder,
        theme_encoder,
        hid_size: int,
    ):
        super().__init__()

        self.executor_encoder = executor_encoder
        self.theme_encoder = theme_encoder

        self.tokenizer = tokenizer
        self.language_model = language_model
        self.heads = ClassifierHeads(
            len(self.executor_encoder.classes_),
            len(self.theme_encoder.classes_),
            hid_size,
        )

    def forward(self, tokens):
        embeddings = self.language_model(**tokens)["last_hidden_state"][
            :, -1, :
        ]

        return self.heads(embeddings)

    def predict(self, message, device="cpu"):
        was_in_training = self.training
        self.eval()

        with torch.no_grad():
            tokens = self.tokenizer(
                message,
                padding=True,
                truncation="only_first",
                return_tensors="pt",
            ).to(device)

            executor_logits, theme_logits = self.forward(tokens)

        executor = np.argmax(executor_logits.detach().cpu().numpy(), axis=1)
        theme = np.argmax(theme_logits.detach().cpu().numpy(), axis=1)

        self.train(was_in_training)

        return (
            self.executor_encoder.inverse_transform(executor),
            self.theme_encoder.inverse_transform(theme),
        )


def evaluate_classifier(
    classifier, dataloader, classifier_loss, device
) -> (float, float):
    """
    Calculate metrics for the classifier.
    """

    # Exit training mode.
    was_in_training = classifier.training
    classifier.eval()

    # Targets and predictions.
    y_all_1 = []
    y_all_2 = []
    y_pred_all_1 = []
    y_pred_all_2 = []

    with torch.no_grad():
        avg_loss = 0.0
        total_samples = 0
        for index, batch in enumerate(dataloader):
            message, executor, theme = batch
            batch_size = theme.shape[0]

            tokens = classifier.tokenizer(
                message,
                padding=True,
                truncation="only_first",
                return_tensors="pt",
            ).to(device)

            y_pred_1, y_pred_2 = classifier(tokens)
            _loss = classifier_loss((y_pred_1, y_pred_2), (executor, theme))

            avg_loss += _loss.item() * batch_size
            total_samples += batch_size

            y_pred_all_1.append(y_pred_1.detach().cpu().numpy())
            y_pred_all_2.append(y_pred_2.detach().cpu().numpy())

            y_all_1.append(executor.detach().cpu().numpy())
            y_all_2.append(theme.detach().cpu().numpy())

        avg_loss /= total_samples

    # F1 score
    y_pred_all_1 = np.argmax(np.vstack(y_pred_all_1), axis=1)
    y_pred_all_2 = np.argmax(np.vstack(y_pred_all_2), axis=1)

    y_all_1 = np.concatenate(y_all_1)
    y_all_2 = np.concatenate(y_all_2)

    f1_score_1 = f1_score(y_all_1, y_pred_all_1, average="weighted")
    f1_score_2 = f1_score(y_all_2, y_pred_all_2, average="weighted")

    # Return to the original mode.
    classifier.train(was_in_training)

    return avg_loss, 0.5 * (f1_score_1 + f1_score_2)
