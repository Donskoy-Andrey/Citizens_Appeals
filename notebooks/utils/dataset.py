import torch


class MessagesDataset(torch.utils.data.Dataset):
    def __init__(self, messages, executors, themes, groups):
        assert len(messages) == len(executors) == len(themes) == len(groups)

        self.messages = messages
        self.executors = executors
        self.themes = themes
        self.groups = groups

    def __len__(self):
        return len(self.executors)

    def __getitem__(self, idx):
        return (
            self.messages[idx],
            self.executors[idx],
            self.themes[idx],
            self.groups[idx],
        )


def prepare_data_for_dataset(data):
    """
    Prepares the data to be converted into a dataset
    """

    return (
        torch.tensor(data["Исполнитель"].to_numpy(), dtype=torch.int64),
        torch.tensor(data["Группа тем"].to_numpy(), dtype=torch.int64),
        data["Текст инцидента"].tolist(),
        torch.tensor(data["Тема"].to_numpy(), dtype=torch.int64),
    )
