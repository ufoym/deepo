# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python
from .tensorflow import Tensorflow


@dependency(Python, Tensorflow)
@source('pip')
class Keras(Module):

    def build(self):
        return r'''
            $PIP_INSTALL \
                h5py \
                keras \
                && \
        '''
