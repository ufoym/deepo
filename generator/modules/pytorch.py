# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Pytorch(Module):

    def build(self):
        cuver = 'cpu' if self.composer.cuda_ver is None else f"cu{''.join(self.composer.cuda_ver.split('.')[:2])}"
        return r'''
            $PIP_INSTALL \
                future \
                numpy \
                protobuf \
                pyyaml \
                && \
            $PIP_INSTALL \
                torch torchvision torchaudio \
                --extra-index-url https://download.pytorch.org/whl/%s \
                && \
        ''' % cuver
