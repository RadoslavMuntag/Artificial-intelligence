import numpy as np


class Optimizer:
    def update(self, weights, d_weights, bias, d_bias):
        raise NotImplementedError


class SGD(Optimizer):
    def __init__(self, velocity=0.1):
        self.v = velocity

    def update(self, weights, d_weights, bias, d_bias):
        weights -= self.v * d_weights
        bias -= self.v * d_bias
        return weights, bias


class SGDMomentum(Optimizer):
    def __init__(self, learning_rate=0.1, momentum=0.9):

        self.v = learning_rate
        self.momentum = momentum
        self.velocity_weights = None
        self.velocity_bias = None

    def update(self, weights, d_weights, bias, d_bias):
        if self.velocity_weights is None:
            self.velocity_weights = np.zeros_like(weights)
        if self.velocity_bias is None:
            self.velocity_bias = np.zeros_like(bias)

        self.velocity_weights = self.momentum * self.velocity_weights - self.v * d_weights
        self.velocity_bias = self.momentum * self.velocity_bias - self.v * d_bias

        weights += self.velocity_weights
        bias += self.velocity_bias

        return weights, bias