# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@source('pip')
@version('0.3.0')
class Pytorch(Module):

    def build(self):
        pyver = self.composer.ver(Python)
        platform = 'cp35-cp35m' if pyver == '3.5' else (
            'cp36-cp36m' if pyver == '3.6' else 'cp27-cp27mu')
        return r'''
            $PIP_INSTALL \
                http://download.pytorch.org/whl/cu80/''' \
        + r'''torch-%s.post4-%s-linux_x86_64.whl \
                torchvision \
                && \
        ''' % (self.version, platform)
