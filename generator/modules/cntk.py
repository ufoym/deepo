# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@source('pip')
@version('2.3')
class Cntk(Module):

    def build(self):
        pyver = self.manager.ver(Python)
        platform = 'cp35-cp35m' if pyver == '3.5' else (
            'cp36-cp36m' if pyver == '3.6' else 'cp27-cp27mu')
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                openmpi-bin \
                libpng-dev \
                libtiff-dev \
                libjasper-dev \
                && \

            $PIP_INSTALL \
                https://cntk.ai/PythonWheel/GPU/cntk-%s-%s-linux_x86_64.whl \
                && \
        ''' % (self.version, platform)
