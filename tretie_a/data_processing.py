import numpy as np
import pandas as pd

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import torch
from torch.utils.data import Dataset, DataLoader


class CHDataset(Dataset):
    def __init__(self, features, targets):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.targets = torch.tensor(targets, dtype=torch.float32)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]


def load_data(batch_size, log_transform_target):
    '''
    vráti predžuté dáta
    :param batch_size:
    :param log_transform_target:
    :return:
    '''
    data = fetch_california_housing()
    X = data.data
    y = data.target

    # rozdelenie dát na trénovacie a testovacie v pomere 8:2
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

    # štandardné škálovanie dát
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    if log_transform_target:
        y_train = np.log(y_train)
        y_test = np.log(y_test)

    train_dataset = CHDataset(X_train, y_train)
    test_dataset = CHDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_dataset, test_dataset, train_loader, test_loader
