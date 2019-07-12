# coding: utf8
''''
author: Huangyuliang
'''
import json
import random
import sys
import numpy as np
import my_datas_loader


#### Define the quadratic and cross-entropy cost functions
class CrossEntropyCost(object):
    @staticmethod
    def fn(a, y):
        return np.sum(np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a)))

    @staticmethod
    def delta(z, a, y):
        return (a - y)


#### Main Network class
class Network(object):
    def __init__(self, sizes, cost=CrossEntropyCost):

        self.num_layers = len(sizes)
        self.sizes = sizes
        self.default_weight_initializer()
        self.cost = cost


    def default_weight_initializer(self):

        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]

        self.weights = [np.random.randn(y, x) / np.sqrt(x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]


    def large_weight_initializer(self):

        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feedforward(self, a):
        """Return the output of the network if ``a`` is input."""

        for b, w in zip(self.biases[:-1], self.weights[:-1]):  # 前n-1层
            a = sigmoid(np.dot(w, a) + b)

        b = self.biases[-1]  # 最后一层
        w = self.weights[-1]
        #a = sigmoid(np.dot(w, a) + b)
        a=np.dot(w, a) + b
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            lmbda=0.0,
            evaluation_data=None,
            monitor_evaluation_accuracy=False):  # 用随机梯度下降算法进行训练

        n = len(training_data)

        for j in range(epochs):
            #random.shuffle(training_data)
            print('---------------------------------------------------------------------%d' % j)
            mini_batches = training_data

            for mini_batch in mini_batches:

                self.update_mini_batch(mini_batch, eta, lmbda, len(training_data))
            print("Epoch %s training complete" % j)

            if monitor_evaluation_accuracy:
                print("Accuracy on evaluation data: {} / {}".format(self.accuracy(evaluation_data), j))

    def update_mini_batch(self, mini_batch, eta, lmbda, n):
        """Update the network's weights and biases by applying gradient
        descent using backpropagation to a single mini batch.  The
        ``mini_batch`` is a list of tuples ``(x, y)``, ``eta`` is the
        learning rate, ``lmbda`` is the regularization parameter, and
        ``n`` is the total size of the training data set.
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]


        #for x, y in mini_batch:
        x=mini_batch[0]

        y=mini_batch[1]

        delta_nabla_b, delta_nabla_w = self.backprop(x, y)
        nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
        nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [(1 - eta * (lmbda / n)) * w - (eta / len(mini_batch)) * nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (eta / len(mini_batch)) * nb
                       for b, nb in zip(self.biases, nabla_b)]

    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # feedforward
        activation = x
        activations = [x]  # list to store all the activations, layer by layer
        zs = []  # list to store all the z vectors, layer by layer

        for b, w in zip(self.biases[:-1], self.weights[:-1]):  # 正向传播 前n-1层

            z = np.dot(w, activation)+b


            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        # 最后一层，不用非线性
        b = self.biases[-1]
        w = self.weights[-1]
        z = np.dot(w, activation) + b
        zs.append(z)
        activation = z
        activations.append(activation)
        # backward pass 反向传播

        sp=sigmoid_prime(zs[-1])
        delta = (self.cost).delta(zs[-1], activations[-1], y)  # 误差 Tj - Oj

        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())  # (Tj - Oj) * O(j-1)

        for l in range(2, self.num_layers):

            z = zs[-l]  # w*a + b
            sp = sigmoid_prime(z)  # z * (1-z)

            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp  # z*(1-z)*(Err*w) 隐藏层误差

            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())  # Errj * Oi
        return (nabla_b, nabla_w)

    def accuracy(self, data):

        results = [(self.feedforward(x), y) for (x, y) in data]
        #alist = [np.sqrt((x[0][0] - y[0]) ** 2 + (x[1][0] - y[1]) ** 2) for (x, y) in results]
        num=0
        for (x,y) in results:
            #print(x,y)
            if(int(x+0.5)==y):
                num+=1
        return num/len(results)

        #return np.mean(alist)

    def save(self, filename):
        """Save the neural network to the file ``filename``."""
        data = {"sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.biases],
                "cost": str(self.cost.__name__)}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()


#### Loading a Network
def load(filename):
    """Load a neural network from the file ``filename``.  Returns an
    instance of Network.
    """
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    net = Network(data["sizes"], cost=cost)
    net.weights = [np.array(w) for w in data["weights"]]
    net.biases = [np.array(b) for b in data["biases"]]
    return net


def sigmoid(z):
    """The sigmoid function."""
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z) * (1 - sigmoid(z))