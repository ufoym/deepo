# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Tensorflow(Module):

    def build(self):
        is_gpu = '' if self.composer.cuda_ver is None else '-gpu'
        return r'''
            $PIP_INSTALL \
                tf-nightly%s-2.0-preview \
                && \
        ''' % is_gpu

    def expose(self):
        return [
            6006,  # expose port for TensorBoard
        ]
