# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .tools import Tools


@dependency(Tools)
@version('3.8')
@source('apt')
class Python(Module):

    def __init__(self, manager, **args):
        super(self.__class__, self).__init__(manager, **args)
        if float(self.version) < 3.8:
            raise NotImplementedError('Only support python >= 3.8 currently.')

    def build(self):
        return (
            r'''
            apt-get update && \
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                python%s \
                python%s-dev \
                python%s-distutils \
                && \
            wget -O ~/get-pip.py \
                https://bootstrap.pypa.io/get-pip.py && \
            python%s ~/get-pip.py && \
            ln -s /usr/bin/python%s /usr/local/bin/python && \
            ''' % tuple([self.version] * 5)
        ).rstrip() + (r'''
            $PIP_INSTALL \
                numpy \
                scipy \
                pandas \
                scikit-image \
                scikit-learn \
                matplotlib \
                Cython \
                tqdm \
                && \
            '''
        ).rstrip()
