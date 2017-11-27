# -*- coding: utf-8 -*-
from .__module__ import Module, source


@source('apt')
class Tools(Module):

    def __repr__(self):
        return ''

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                build-essential \
                ca-certificates \
                cmake \
                wget \
                git \
                vim \
                && \
            '''
