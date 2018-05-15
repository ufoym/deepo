# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .tools import Tools
from .python import Python


@dependency(Tools, Python)
@source('git')
@version('1.0.1')
class Theano(Module):

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libblas-dev \
                && \

            wget -qO- https://github.com/Theano/Theano/archive/rel-%s.tar.gz''' \
            % self.version + r''' | tar xz -C ~ && \
            cd ~/Theano* && \
            $PIP_INSTALL \
                . && \
        ''' + (
            '' if self.composer.cuda_ver is None else r'''
            $GIT_CLONE https://github.com/Theano/libgpuarray ~/gpuarray && \
            mkdir -p ~/gpuarray/build && cd ~/gpuarray/build && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  .. && \
            make -j"$(nproc)" install && \
            cd ~/gpuarray && \
            python setup.py build && \
            python setup.py install && \

            printf '[global]\nfloatX = float32\ndevice = cuda0\n\n[dnn]\n'''
            + r'''include_path = /usr/local/cuda/targets'''
            + r'''/x86_64-linux/include\n' > ~/.theanorc && \
        ''')
