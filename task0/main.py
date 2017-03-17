#!/usr/bin/env python3

import numpy as np


def main():
    col_id, features, y = get_train_data('data/train.csv')
    model = train(features, y)
    print(calc_error(predict(model, features), y))


    col_id, features = get_test_data('data/test.csv')
    predictions = predict(model, features)

    write_result(col_id, predictions)


def csv_to_array(filename):
    """
    Returns contents of `filename` CSV file as a numpy array.

    Assumes and ignores exactly one header line
    """
    return np.genfromtxt(
        filename, delimiter=',', dtype=np.longdouble, skip_header=True
    )


def get_train_data(filename):
    data = csv_to_array(filename)
    col_id = data[:, 0].astype('int')
    y = data[:, 1]
    features = data[:, 2:]
    return col_id, features, y


def get_test_data(filename):
    data = csv_to_array(filename)
    col_id = data[:, 0].astype('int')
    features = data[:, 1:]
    return col_id, features


def train(features, output):
    return mymean


def mymean(v):
    v.sort()
    return np.mean(v)


def predict(model, test_set):
    return np.apply_along_axis(model, 1, test_set)


def calc_error(predictions, true_values):
    errors = true_values - predictions
    return (np.sum(errors ** 2) / errors.size) ** 0.5


def write_result(col_id, predictions):
    result_test = np.column_stack((col_id, predictions))
    np.savetxt(
        "test_result.csv", result_test,
        header="Id,y", comments="",
        delimiter=",", fmt="%i,%r"
    )


if __name__ == '__main__':
    main()
