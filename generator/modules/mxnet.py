# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Mxnet(Module):

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libatlas-base-dev \
                graphviz \
                && \

            $PIP_INSTALL \
                mxnet%s \
                graphviz \
                && \
        ''' % ('' if self.composer.cpu_only else '-cu90')
