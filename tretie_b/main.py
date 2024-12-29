import numpy as np
import matplotlib.pyplot as plt

from mse import MSE
from optimizer import *
from activ_func import *

THE_INPUT = np.array([
    [0, 1, 0, 1],
    [0, 0, 1, 1]
])

XOR_output = np.array([0, 1, 1, 0])
AND_output = np.array([0, 0, 0, 1])
OR_output = np.array([0, 1, 1, 1])


class Layer:
    def __init__(self, input_size, output_size, active_func: ActivFunc = TanH(), optimizer: Optimizer = SGDMomentum()):
        self.weights: np.ndarray = np.random.randn(output_size, input_size)
        self.bias: np.ndarray = np.zeros((output_size, 1))
        self.received_input = None
        self.d_weights = []
        self.d_bias = []

        self.active_func: ActivFunc = active_func
        self.optimizer: Optimizer = optimizer

    def forward(self, input_data):
        self.received_input = input_data
        out = self.weights.dot(input_data) + self.bias
        out = self.active_func.forward(out)

        return out

    def backward(self, output_gradient):
        output_gradient = self.active_func.backward(output_gradient)
        self.d_weights = output_gradient.dot(self.received_input.T)
        self.d_bias = np.sum(output_gradient)

        return self.weights.T.dot(output_gradient)

    def update_parameters(self):
        self.weights, self.bias = self.optimizer.update(self.weights, self.d_weights, self.bias, self.d_bias)


class Model:
    def __init__(self):
        self.layers: list[Layer] = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def forward(self, input_data):
        for layer in self.layers:
            input_data = layer.forward(input_data)

        return input_data

    def backward(self, output_gradient):
        for layer in reversed(self.layers):
            output_gradient = layer.backward(output_gradient)

    def update_parameters(self):
        for layer in self.layers:
            layer.update_parameters()


# FUNKCIE NA ZVLÁDANIE POUŽÍVATEĽSKÉHO INPUTU ------------------------------------
def set_training_problem():
    problems = [
        XOR_output,
        AND_output,
        OR_output
    ]
    while True:
        try:
            problem_id = int(input("Select problem for training (0: XOR [DEFAULT], 1: AND, 2: OR): ") or 0)
            assert 0 <= problem_id < 3
            return problems[problem_id]
        except (ValueError, AssertionError, TypeError):
            print("Invalid input. Try again.")


def set_number_of_layers():
    while True:
        try:
            layer_count = int(input("Select number of hidden layers (more than 0) [1 DEFAULT]: ") or 1)
            assert layer_count > 0
            return layer_count
        except (ValueError, AssertionError, TypeError):
            print("Invalid input. Try again.")


def set_number_of_neurons_per_layer():
    while True:
        try:
            neuron_count = int(input("Select number of neurons per layer (more than 0) [4 DEFAULT]: ") or 4)
            assert neuron_count > 0
            return neuron_count
        except (ValueError, AssertionError, TypeError):
            print("Invalid input. Try again.")


def set_sgd():
    while True:
        try:
            sgd_id = int(input("Choose SDG (0: no momentum, 1: with momentum [DEFAULT]): ") or 1)
            assert sgd_id == 0 or sgd_id == 1
            return sgd_id
        except (ValueError, AssertionError, TypeError):
            print("Invalid input. Try again.")


def set_activation_function(local_model: Model, neuron_count: int, sgd_id: int, index: int, last: bool = False):
    functions = [
        Sigmoid(),
        TanH(),
        ReLU()
    ]
    sgds = [
        SGD(),
        SGDMomentum()
    ]
    while True:
        try:
            function_id = None
            if last:
                function_id = int(input(f"Choose activation function for output layer (0: Sigmoid, 1: Tanh [DEFAULT], "
                                        f"2: ReLU): ") or 1)
            else:
                function_id = int(input(f"Choose activation function for layer {index + 1} (0: Sigmoid, 1: Tanh ["
                                        f"DEFAULT], 2: ReLU): ") or 1)
            assert 0 <= function_id < 3
            if index == 0:
                local_model.add_layer(Layer(2, neuron_count, functions[function_id], sgds[sgd_id]))
            elif last:
                local_model.add_layer(Layer(neuron_count, 1, functions[function_id], sgds[sgd_id]))
            else:
                local_model.add_layer(Layer(neuron_count, neuron_count, functions[function_id], sgds[sgd_id]))
            return
        except (ValueError, AssertionError, TypeError):
            print("Invalid input. Try again.")


if __name__ == "__main__":
    loss_plot = []
    epoch_plot = []

    model = Model()
    loss_function = MSE()

    print("leave blank for [DEFAULT].")
    expected_output = set_training_problem()
    layers = set_number_of_layers()
    neurons = set_number_of_neurons_per_layer()
    sgd = set_sgd()

    # priraďovanie vrstiev
    for i in range(layers):
        set_activation_function(model, neurons, sgd, i, False)
    # výstupná vrstva
    set_activation_function(model, neurons, sgd, -1, True)

    for epoch in range(500):
        generated_output = model.forward(THE_INPUT)
        loss = loss_function.forward(generated_output, expected_output)

        loss_gradient = loss_function.backward()
        model.backward(loss_gradient)

        model.update_parameters()

        print("Generated output", np.round(generated_output, decimals=3).flatten().tolist())
        print("Expected output", expected_output)
        print(f"Epoch {epoch}, Loss: {loss}")
        loss_plot.append(loss)
        epoch_plot.append(epoch)
        print("")

    plt.plot(epoch_plot, loss_plot)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Model learning curve')

    plt.show()
