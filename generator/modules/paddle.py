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
                paddlepaddle%s-latest-cp%s-cp%sm-linux_x86_64.whl \
                && \
        ''' % ('' if self.composer.cuda_ver is None else '_gpu', pyver, pyver)
