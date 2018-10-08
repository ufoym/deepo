# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools
from .python import Python
from .opencv import Opencv


@dependency(Tools, Python, Opencv)
@source('git')
class Caffe2(Module):

    def build(self):
        switcher = 'OFF' if self.composer.cuda_ver is None else 'ON'
        pyver = self.composer.ver(Python)
        platform = 'cp35-cp35m' if pyver == '3.5' else (
            'cp36-cp36m' if pyver == '3.6' else 'cp27-cp27mu')
        cuver = 'cpu' if self.composer.cuda_ver is None else 'cu%d' % (
            float(self.composer.cuda_ver) * 10)

        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libprotobuf-dev \
                protobuf-compiler \
                && \

            $PIP_INSTALL \
                future \
                numpy \
                protobuf \
                enum34 \
                pyyaml \
                typing \
                && \

        ''' + (r'''
            wget -O ~/caffe2.tar.xz \
                https://github.com/ufoym/prebuild/raw/caffe2/caffe2-master-%s-%s-linux_x86_64.tar.xz && \
            tar -xvf ~/caffe2.tar.xz -C /usr/local/lib && \
        ''' % (cuver, platform) if cuver in ['cu90'] and platform in ['cp27-cp27mu', 'cp36-cp36m'] else r'''
            $GIT_CLONE https://github.com/pytorch/pytorch.git \
                ~/caffe2 --branch master --recursive && \
            cd ~/caffe2 && mkdir build && cd build && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  -D USE_CUDA=%s \
                  -D USE_MPI=OFF \
                  -D USE_NNPACK=OFF \
                  -D USE_ROCKSDB=OFF \
                  -D BUILD_TEST=OFF \
                  .. && \
            make -j"$(nproc)" install && \
        ''' % switcher)
