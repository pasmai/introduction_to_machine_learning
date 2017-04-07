import abc

from sklearn import metrics
import numpy as np


class _AbstractLearner(object):

    __metaclass__ = abc.ABCMeta

    _model = NotImplemented

    # _train_features and _train_outputs are NumPy arrays
    def __init__(self):
        self._train_features = None
        self._train_outputs = None

    # Calls self._train
    def learn_from(self, features, outputs):
        self._train_features = features
        self._train_outputs = outputs
        self._train()

    @abc.abstractmethod
    def predict_from(self, features, outputs):
        raise NotImplementedError

    # Calls self.predict_from
    def validate_against(self, features, outputs):
        predictions = self.predict_from(features)
        return self.accuracy(predictions, outputs)

    @property
    # Calls self.predict_from
    def train_error(self):
        predictions = self.predict_from(self._train_features)
        return self.accuracy(predictions, self._train_outputs)

    @staticmethod
    def accuracy(predictions, true_values):
        return metrics.accuracy_score(predictions, true_values)

    @abc.abstractmethod
    def _train(self):
        raise NotImplementedError


class SciKitLearner(_AbstractLearner):

    _scale     = None
    _transform = None

    def predict_from(self, features):
        if hasattr(self._scale, 'transform'):
            features = self._scale.transform(features)
        if hasattr(self._transform, 'transform'):
            features = self._transform.transform(features)
        return self._model(features)
