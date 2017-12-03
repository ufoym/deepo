# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Tensorflow(Module):

    def build(self):
        return r'''
            $PIP_INSTALL \
                tensorflow%s \
                && \
        ''' % ('' if self.composer.cpu_only else '_gpu')

    def expose(self):
        return [
            6006,  # expose port for TensorBoard
        ]
