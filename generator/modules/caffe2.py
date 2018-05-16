# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools
from .python import Python
from .opencv import Opencv


@dependency(Tools, Python, Opencv)
@source('git')
class Caffe2(Module):

    def build(self):
        pyver = self.composer.ver(Python)
        switcher = 'OFF' if self.composer.cuda_ver is None else 'ON'
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libprotobuf-dev \
                protobuf-compiler \
                openmpi-bin \
                && \

            $PIP_INSTALL \
                future \
                numpy \
                protobuf \
                && \

            $GIT_CLONE https://github.com/pytorch/pytorch.git \
                ~/caffe2 --recursive && \
            git submodule update --init && \

            cd ~/caffe2 && \
            sed -i "s/prefix=''/prefix='', standard_lib=True) \
                + '\/dist-packages'/g" CMakeLists.txt && \

            mkdir build && cd build && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  -D USE_CUDA=%s \
                  -D USE_MPI=%s \
                  .. && \
            make -j"$(nproc)" install && \
            %s
        ''' % (
            switcher,
            switcher,

            '' if pyver == '2.7' else (r'''
            mv /usr/local/lib/python3/dist-packages/caffe2 \
                /usr/local/lib/python%s/dist-packages && \
            ''' % pyver).strip()
            )
