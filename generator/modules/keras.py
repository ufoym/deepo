# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python
from .tensorflow import Tensorflow


@dependency(Python, Tensorflow)
@source('pip')
class Keras(Module):

    def build(self):
        return r'''
            # Now Keras comes packaged with TensorFlow 2
            # as tensorflow.keras. To start using Keras,
            # simply install TensorFlow 2.
        '''
