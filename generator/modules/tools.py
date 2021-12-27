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
                apt-utils \
                ca-certificates \
                wget \
                git \
                vim \
                libssl-dev \
                curl \
                unzip \
                unrar \
                cmake \
                && \
            '''
