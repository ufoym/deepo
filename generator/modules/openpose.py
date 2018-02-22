# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python
from .caffe import Caffe
from .opencv import Opencv


@dependency(Caffe, Opencv)
@source('git')
class Openpose(Module):

    def build(self):
        return r'''
            $GIT_CLONE https://github.com/CMU-Perceptual-Computing-Lab/openpose.git /openpose && \
            sed -i 's/set(Caffe_known_gpu_archs "20 21(20) 30 35 50 52 60 61")/set(Caffe_known_gpu_archs "30 35 50 52 60 61 70")/g' /openpose/cmake/Cuda.cmake && \
            mkdir -p /openpose/build && cd /openpose/build && \
            cmake -DBUILD_CAFFE=OFF \
                  -DCaffe_INCLUDE_DIRS=/usr/local/include \
                  -DCaffe_LIBS=/usr/local/lib/libcaffe.so \
                  -DOpenCV_INCLUDE_DIRS=/usr/local/include \
                  -DOpenCV_LIBS_DIR=/usr/local/lib \
                  -DDOWNLOAD_HAND_MODEL=OFF \
                  -DDOWNLOAD_FACE_MODEL=OFF \
                  -DDOWNLOAD_COCO_MODEL=ON .. && \
            make -j"$(nproc)" && \
            make install && \
        '''
