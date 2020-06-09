# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@source('pip')
class Paddle(Module):

    def build(self):
        pyver = self.composer.ver(Python)
        pyver = pyver.replace('.', '')
        return r'''
            $PIP_INSTALL \
                https://paddle-wheel.bj.bcebos.com/0.0.0-%s-mkl/paddlepaddle%s-0.0.0-cp%s-cp%sm-linux_x86_64.whl \
                && \
        ''' % (
            'cpu' if self.composer.cuda_ver is None else 'gpu-cuda10-cudnn7',
            '' if self.composer.cuda_ver is None else '_gpu',
            pyver, pyver)
