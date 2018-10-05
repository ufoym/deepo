# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .python import Python
from .jupyter import Jupyter


@dependency(Python, Jupyter)
@source('pip')
class Jupyterlab(Module):

    def build(self):
        return r'''
            $PIP_INSTALL \
                jupyterlab \
                && \
        '''
