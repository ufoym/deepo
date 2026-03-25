# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@version('latest')
@source('pip')
class Tensorflow(Module):

    def __init__(self, manager, **args):
        super().__init__(manager, **args)
        if self.version not in ('1.13.1', '2.0.0a0', 'latest'):
            raise NotImplementedError('unsupported tensorflow version')

    def build(self):
        is_gpu = '' if self.composer.cuda_ver is None else '-gpu'
        if self.version == 'latest':
            tensorflow_version = f'tensorflow{is_gpu}'
        else:
            tensorflow_version = f'tensorflow{is_gpu}=={self.version}'
        return r'''
            $PIP_INSTALL \
                %s \
                && \
        ''' % tensorflow_version

    def expose(self):
        return [6006]
