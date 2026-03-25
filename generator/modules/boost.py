# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools
from .python import Python


@dependency(Tools, Python)
@source('src')
class Boost(Module):

    def __repr__(self):
        return ''

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libboost-all-dev \
                && \
        '''
