# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python
from .tensorflow import Tensorflow


@dependency(Python, Tensorflow)
@source('pip')
class Sonnet(Module):

    def build(self):
        return r'''
            $PIP_INSTALL \
                tensorflow_probability \
                "dm-sonnet>=2.0.0b0" --pre \
                && \
        '''
