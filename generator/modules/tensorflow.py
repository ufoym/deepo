# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Tensorflow(Module):

    def build(self):
        tf_version = self.composer.ver(Tensorflow)
        tf_version = '' if 'latest' == tf_version else '==' + tf_version
        is_gpu = '' if self.composer.cpu_only else '-gpu'
        return r'''
            $PIP_INSTALL \
                tensorflow%s%s \
                && \
        ''' % (is_gpu, tf_version)

    def expose(self):
        return [
            6006,  # expose port for TensorBoard
        ]
