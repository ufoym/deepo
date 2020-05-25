# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@source('pip')
class Paddle(Module):

    def build(self):
        return r'''
            $PIP_INSTALL \
                paddlepaddle%s \
                && \
        ''' % ('' if self.composer.cuda_ver is None else '-gpu')
