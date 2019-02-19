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
        pyver = self.composer.ver(Python)
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libboost-all-dev \
                && \
            ''' if pyver == '2.7' else (
            r'''
            wget -O ~/boost.tar.gz '''
            + r'''https://dl.bintray.com/boostorg/release/1.69.0'''
            + r'''/source/boost_1_69_0.tar.gz && \
            tar -zxf ~/boost.tar.gz -C ~ && \
            cd ~/boost_* && \
            ./bootstrap.sh --with-python=python%s && \
            ./b2 install --prefix=/usr/local && \
            ''' % pyver
        )
