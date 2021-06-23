# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools


@dependency(Tools)
@source('git')
class Darknet(Module):

    def build(self):
        use_gpu = 1 if self.composer.cuda_ver else 0

        return r'''
            $GIT_CLONE https://github.com/AlexeyAB/darknet ~/darknet && \
            cd ~/darknet && \
            sed -i 's/GPU=0/GPU=%d/g' ~/darknet/Makefile && \
            sed -i 's/CUDNN=0/CUDNN=%d/g' ~/darknet/Makefile && \
            make -j"$(nproc)" && \
            cp ~/darknet/include/* /usr/local/include && \
            cp ~/darknet/darknet /usr/local/bin && \
        ''' % (use_gpu, use_gpu)
