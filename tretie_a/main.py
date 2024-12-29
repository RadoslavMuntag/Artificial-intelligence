import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import yaml

from data_processing import CHDataset, load_data

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


class NeuralNetwork(nn.Module):
    def __init__(self, the_model):
        super(NeuralNetwork, self).__init__()
        self.model = the_model

    def forward(self, x):
        return self.model(x)


def train_loop(model: NeuralNetwork, train_loader, criterion, optimizer: optim, num_epochs=50):
    '''
    trénovanie modelu
    :param model:
    :param train_loader:
    :param criterion:
    :param optimizer:
    :param num_epochs:
    :return:
    '''
    train_losses = []

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for inputs, targets in train_loader:
            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs.squeeze(), targets)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        epoch_loss = running_loss / len(train_loader)
        train_losses.append(epoch_loss)
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {running_loss / len(train_loader)}")

    plt.plot(range(1, num_epochs + 1), train_losses, label="Training Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.show()


def evaluate_model(model: NeuralNetwork, test_loader, criterion, output_file="predictions.csv"):
    '''
    ecaluácia modelu
    :param model:
    :param test_loader:
    :param criterion:
    :param output_file:
    :return:
    '''
    model.eval()
    test_loss = 0.0
    all_predictions = []
    all_targets = []

    with torch.no_grad():
        for inputs, targets in test_loader:
            outputs = model(inputs)
            loss = criterion(outputs.squeeze(), targets)
            test_loss += loss.item()

            all_predictions.extend(outputs.squeeze().tolist())
            all_targets.extend(targets.tolist())

    if config["preprocessing"]["log_transform_target"]:
        all_predictions = np.exp(all_predictions)
        all_targets = np.exp(all_targets)

    all_predictions = np.round(all_predictions, decimals=4)
    all_targets = np.round(all_targets, decimals=4)
    print(f"Test Loss: {test_loss / len(test_loader)}")

    predictions_df = pd.DataFrame({
        "Actual": all_targets,
        "Predicted": all_predictions,
        "Difference": all_targets - all_predictions
    })
    predictions_df.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")


def get_sequential_model(layers_config):
    '''
    vráti skvenčný model s vrstvami podľa konfigurácie
    :param layers_config:
    :return:
    '''
    layers = []
    last_layer = None
    for i in layers_config:
        layer = layers_config[i]
        if last_layer is None:
            layers.append(nn.Linear(8, layer["layer_size"]))
        else:
            layers.append(nn.Linear(last_layer["layer_size"], layer["layer_size"]))

        layers.append(getattr(nn, layer["activation_function"])())
        last_layer = layer

    layers.append(nn.Linear(last_layer["layer_size"], 1))
    # layers.append(getattr(nn, "Tanh")())

    return nn.Sequential(*layers)


if __name__ == '__main__':
    train_data, test_data, train_loader, test_loader = load_data(config["training"]["batch_size"],
                                                                 config["preprocessing"]["log_transform_target"])

    model = NeuralNetwork(get_sequential_model(config["model"]["hidden_layers"]))

    criterion = nn.MSELoss()

    optimizer = None
    # priradenie optimalizačného algoritmu z konfigurácie
    if config["optimizer"]["type"] == "SGD":
        current_opt = config["optimizer"]["sgd_config"]
        optimizer = optim.SGD(model.parameters(), lr=current_opt["learning_rate"])

    elif config["optimizer"]["type"] == "SGD Momentum":
        current_opt = config["optimizer"]["sgd_momentum_config"]
        optimizer = optim.SGD(model.parameters(), lr=current_opt["learning_rate"], momentum=current_opt["momentum"])

    if config["optimizer"]["type"] == "Adam":
        current_opt = config["optimizer"]["adam_config"]
        optimizer = optim.Adam(model.parameters(), lr=current_opt["learning_rate"])

    train_loop(model, train_loader, criterion, optimizer, num_epochs=config["training"]["num_epochs"])
    evaluate_model(model, test_loader, criterion)
