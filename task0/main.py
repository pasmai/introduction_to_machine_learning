#!/usr/bin/env python3

import abc

import numpy as np


class CSVDataSet(object):

    def __init__(self, ids, features, outputs):
        self.ids = ids
        self.features = features
        self.outputs = outputs

    @classmethod
    def from_train_data(cls, filename):
        data = cls._csv_to_array(filename)
        train_id = data[:, 0].astype('int')
        train_y = data[:, 1]
        train_features = data[:, 2:]
        return cls(train_id, train_features, train_y)

    @classmethod
    def from_test_data(cls, filename):
        data = cls._csv_to_array(filename)
        test_id = data[:, 0].astype('int')
        test_features = data[:, 1:]
        return cls(test_id, test_features, None)

    @staticmethod
    def _csv_to_array(filename, dtype=np.longdouble):
        """
        Returns contents of `filename` CSV file as a numpy array.

        dtype: NumPy type

        Note: Assumes and ignores exactly one header line.
        """
        return np.genfromtxt(
            filename, delimiter=',', dtype=dtype, skip_header=True
        )

    def write_labelled_output(self, filename):
        np.savetxt(
            filename, np.column_stack((self.ids, self.outputs)),
            header="Id,y", comments="",
            delimiter=",", fmt="%i,%r"
        )


class AbstractLearner(object):

    __metaclass__ = abc.ABCMeta

    _model = NotImplemented

    def __init__(self):
        self._train_set = None
        self._test_set = None

    def learn_from(self, train_set):
        self._train_set = train_set
        self._train()

    def predict_from(self, test_set):
        self._test_set = test_set
        return self._predict()

    @staticmethod
    def rms_error(predictions, true_values):
        errors = true_values - predictions
        return (np.sum(errors ** 2) / errors.size) ** 0.5

    @abc.abstractmethod
    def _train(self):
        raise NotImplementedError

    def _predict(self):
        self._test_set.outputs = np.apply_along_axis(
            self._model, 1, self._test_set.features
        )
        return self._test_set


class MeanLearner(AbstractLearner):

    def _train(self):
        self._model = np.mean


class AdvMeanLearner(AbstractLearner):

    def _train(self):
        self._model = _mymean

    @staticmethod
    def _mymean(v):
        v.sort()
        return np.mean(v)


def main():
    train_set = CSVDataSet.from_train_data('data/train.csv')
    test_set = CSVDataSet.from_test_data('data/test.csv')

    learner = MeanLearner()
    learner.learn_from(train_set)
    out_set = learner.predict_from(test_set)
    out_set.write_labelled_output('test_result.csv')

    #print(calc_error(predict(model, features), y))


if __name__ == '__main__':
    main()
