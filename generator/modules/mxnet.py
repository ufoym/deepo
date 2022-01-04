# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Mxnet(Module):

    def build(self):
        cuver = '' if self.composer.cuda_ver is None else '-cu%s' % ''.join(self.composer.cuda_ver.split('.')[:2])
        if cuver == '-cu113':
            cuver = '-cu112' # mxnet does not support cu113
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libatlas-base-dev \
                graphviz \
                && \

            $PIP_INSTALL \
                mxnet%s \
                graphviz \
                && \
        ''' % cuver
