# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools
from .boost import Boost
from .python import Python
from .opencv import Opencv


@dependency(Tools, Python, Boost, Opencv)
@source('git')
class Caffe(Module):

    def build(self):
        cpu_only = self.composer.cuda_ver is None
        return (r'''
            apt-get update && \
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                caffe-%s \
                && \
        ''' % ('cpu' if cpu_only else 'cuda')
        ).rstrip()
