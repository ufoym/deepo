# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python
from .opencv import Opencv


@dependency(Python, Opencv)
@source('pip')
class Cntk(Module):

    def build(self):
        pyver = self.composer.ver(Python)
        platform = 'cp35-cp35m' if pyver == '3.5' else (
            'cp36-cp36m' if pyver == '3.6' else 'cp27-cp27mu')
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                openmpi-bin \
                libpng-dev \
                libtiff-dev \
                libjasper-dev \
                && \

            wget --no-verbose -O - https://github.com/01org/mkl-dnn/releases/download/v0.14/mklml_lnx_2018.0.3.20180406.tgz | tar -xzf - && \
            cp mklml*/* /usr/local -r && \

            wget --no-verbose -O - https://github.com/01org/mkl-dnn/archive/v0.14.tar.gz | tar -xzf - && \
            cd mkl-dnn-0.14 && mkdir build && cd build && \
            ln -s /usr/local external && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  .. && \
            make -j"$(nproc)" install && \

            $PIP_INSTALL \
                cntk%s \
                && \
        ''' % ('' if self.composer.cuda_ver is None else '-gpu')
