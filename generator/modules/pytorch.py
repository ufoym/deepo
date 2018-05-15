# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@source('pip')
@version('0.4.0')
class Pytorch(Module):

    def build(self):
        pyver = self.composer.ver(Python)
        cuver = 'cpu' if self.composer.cuda_ver is None else 'cu%d' % (
            float(self.composer.cuda_ver) * 10)
        platform = 'cp35-cp35m' if pyver == '3.5' else (
            'cp36-cp36m' if pyver == '3.6' else 'cp27-cp27mu')
        return r'''
            $PIP_INSTALL \
                http://download.pytorch.org/whl/%s/''' % cuver \
        + r'''torch-%s-%s-linux_x86_64.whl \
                torchvision \
                && \
        ''' % (self.version, platform)
