# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python


@dependency(Python)
@source('pip')
class Pytorch(Module):

    def build(self):
        cuver = 'cpu' if self.composer.cuda_ver is None else 'cu%s' % ''.join(self.composer.cuda_ver.split('.')[:2])
        return r'''
            $PIP_INSTALL \
                future \
                numpy \
                protobuf \
                enum34 \
                pyyaml \
                typing \
                && \
            $PIP_INSTALL \
                --pre torch torchvision torchaudio -f \
                https://download.pytorch.org/whl/nightly/%s/torch_nightly.html \
                && \
        ''' % cuver
