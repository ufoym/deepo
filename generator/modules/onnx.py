# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Onnx(Module):

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                protobuf-compiler \
                libprotoc-dev \
                && \

            $PIP_INSTALL \
                numpy \
                protobuf \
                onnx \
                onnxruntime%s \
                && \
        ''' % ('' if self.composer.cuda_ver is None else '-gpu')
