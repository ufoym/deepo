# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .python import Python


@dependency(Python)
@version('latest')
@source('pip')
class Spacy(Module):

    def build(self):
        spacyversion = 'spacy'
        if self.composer.cuda_ver is not None:
            spacyversion = "spacy[cuda%d]" % int(float(self.composer.cuda_ver) * 10)

        return r'''
            $PIP_INSTALL \
                %s \
                && \
        ''' % spacyversion
