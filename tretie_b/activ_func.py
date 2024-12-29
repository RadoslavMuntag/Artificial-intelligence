import numpy as np


class ActivFunc:
    def forward(self, input_data):
        raise NotImplementedError

    def backward(self, output_gradient):
        raise NotImplementedError


class Sigmoid(ActivFunc):
    def forward(self, input_data):
        self.last_output = 1 / (1 + np.exp(-input_data))
        return self.last_output

    def backward(self, output_gradient):
        return output_gradient * (self.last_output * (1 - self.last_output))


class ReLU(ActivFunc):
    def forward(self, input_data):
        self.last_input = input_data
        return np.maximum(input_data, 0)

    def backward(self, output_grad):
        return output_grad * (self.last_input > 0)


class TanH(ActivFunc):
    def forward(self, input_data):
        self.last_output = np.tanh(input_data)
        return self.last_output

    def backward(self, output_grad):
        return output_grad * (1 - self.last_output ** 2)