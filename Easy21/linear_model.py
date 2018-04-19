import numpy as np

class LinApproximator:
    def __init__(self, w = None):
        self.w = w

    def __call__(self, x):
        if self.w is None:
            self.w = np.zeros(x.shape)
        return np.matmul(x, self.w)

    def tdl_step(self, target, e_trace, alpha = .01):
        if self.w is None:
            self.w = np.zeros(e_trace.shape)
        self.w += alpha * target * e_trace

