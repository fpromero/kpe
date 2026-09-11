import numpy as np


def owa_aggregation(vector, quantifier, axis=0, keepdims=True):
    '''
    OWA operator that generates the weight vector using a quantifier
    function determined by a and b. (Check std_quantifier() understand this process)

    :param quantifier:
    :param vector: data to aggregate.
    :param a: quantifier parameter 1
    :param b: quantifier parameter 2
    :param axis: axis to reduce.
    :param keepdims: if true, the shape will have the same length.
    :return: matrix with the aggregated axis.
    '''
    X_sorted = np.sort(vector, axis=axis)
    w = 0.0
    if quantifier == "pasi":
        w = generate_owa_weights(len(vector), lambda x: std_quantifier_pasi(x))
    elif quantifier == "feng":
        w = generate_owa_weights(len(vector), lambda x: std_quantifier_feng(x))
    elif quantifier == "alh":
        w = generate_owa_weights(len(vector), lambda x: std_quantifier_at_least_half(x))

    X_agg = np.apply_along_axis(lambda a: np.dot(a, w), axis, X_sorted)
    if keepdims:
        X_agg = np.expand_dims(X_agg, axis=axis)

    return X_agg


def generate_owa_weights(n, quantifier):
    '''
    Quantifier function that generates a vector of weights using a quantifier
    function.

    :param quantifier: quantifier function.
    :return: a vector of weights.
    '''
    weights = np.zeros(n)
    for i in range(n):
        ri = i + 1

        weights[i] = quantifier(ri / n) - quantifier((ri - 1) / n)

    return weights


def std_quantifier_feng(x):
    Q = 0.0
    if 0.5 >= x >= 0:
        return 0

    elif 1 >= x > 0.5:
        Q = (2 * x - 1) ** 0.5

    return Q

def std_quantifier_pasi(x):
    Q = 0.0

    if 0.4 >= x >= 0:
        return 0

    elif 0.9 >= x > 0.4:
        Q = 2 * (x - 0.4)

    elif 1 >= x > 0.9:
        return 1

    return Q

def std_quantifier_avg(x):
    Q = 0.0

    if 0.0 >= x >= 1:
        return Q
    else:
        return 1

    return Q

def std_quantifier_at_least_half(x):
    Q = 0.0

    if 0.5 >= x >= 0:
        return x * 2

    elif 0.1 >= x > 0.5:
        return 1

    return Q
