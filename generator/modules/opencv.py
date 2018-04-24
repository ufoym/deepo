# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .tools import Tools
from .boost import Boost
from .python import Python


@dependency(Tools, Python, Boost)
@source('git')
@version('3.4.1')
class Opencv(Module):

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libatlas-base-dev \
                libgflags-dev \
                libgoogle-glog-dev \
                libhdf5-serial-dev \
                libleveldb-dev \
                liblmdb-dev \
                libprotobuf-dev \
                libsnappy-dev \
                protobuf-compiler \
                && \

            $GIT_CLONE --branch %s https://github.com/opencv/opencv ~/opencv && \
            mkdir -p ~/opencv/build && cd ~/opencv/build && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  -D WITH_IPP=OFF \
                  -D WITH_CUDA=OFF \
                  -D WITH_OPENCL=OFF \
                  -D BUILD_TESTS=OFF \
                  -D BUILD_PERF_TESTS=OFF \
                  .. && \
            make -j"$(nproc)" install && \
        ''' % self.version
