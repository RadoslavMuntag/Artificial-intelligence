import numpy as np


class MSE:
    def __init__(self):
        self.y_generated = None
        self.expected_y = None

    def forward(self, y, expected_y):
        # print("generated answer: ", y, " expected answer: ", expected_y)
        self.y_generated = y
        self.expected_y = expected_y
        return np.mean((y - expected_y) ** 2)

    def backward(self):
        return 2 * (self.y_generated - self.expected_y) / self.expected_y.size
