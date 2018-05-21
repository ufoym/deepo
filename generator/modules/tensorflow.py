# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Tensorflow(Module):

    def build(self):
        tf_version = self.composer.ver(Tensorflow)
        if self.composer.cuda_ver == '8.0':
            tf_version = '1.4'
        tf_version = '' if 'latest' == tf_version else '==' + tf_version
        is_gpu = '' if self.composer.cuda_ver is None else '-gpu'
        return r'''
            $PIP_INSTALL \
                tensorflow%s%s \
                && \
        ''' % (is_gpu, tf_version)

    def expose(self):
        return [
            6006,  # expose port for TensorBoard
        ]
