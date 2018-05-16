# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .tools import Tools


@dependency(Tools)
@version('3.5')
@source('apt')
class Python(Module):

    def __init__(self, manager, **args):
        super(self.__class__, self).__init__(manager, **args)
        if self.version not in ('2.7', '3.5', '3.6',):
            raise NotImplementedError('unsupported python version')

    def build(self):
        return (r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                python3-pip \
                python3-dev \
                && \
            ln -s /usr/bin/python3 /usr/local/bin/python && \
            pip3 --no-cache-dir install --upgrade pip && \
            $PIP_INSTALL \
                setuptools \
                && \
            ''' if self.version == '3.5' else (
            r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                software-properties-common \
                && \
            add-apt-repository ppa:deadsnakes/ppa && \
            apt-get update && \
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                python3.6 \
                python3.6-dev \
                && \
            wget -O ~/get-pip.py \
                https://bootstrap.pypa.io/get-pip.py && \
            python3.6 ~/get-pip.py && \
            ln -s /usr/bin/python3.6 /usr/local/bin/python3 && \
            ln -s /usr/bin/python3.6 /usr/local/bin/python && \
            $PIP_INSTALL \
                setuptools \
                && \
            ''' if self.version == '3.6' else
            r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                python-pip \
                python-dev \
                && \
            $PIP_INSTALL \
                setuptools \
                pip \
                && \
            '''
        )).rstrip() + r'''
            $PIP_INSTALL \
                numpy \
                scipy \
                pandas \
                scikit-learn \
                matplotlib \
                Cython \
                && \
        '''
