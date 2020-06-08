# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools


@dependency(Tools)
@source('git')
class Torch(Module):

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                sudo \
                && \

            $GIT_CLONE https://github.com/nagadomi/distro.git ~/torch --recursive && \
            cd ~/torch && \
            bash install-deps && \
            sed -i 's/${THIS_DIR}\/install/\/usr\/local/g' ./install.sh && \
            ./install.sh && \
        '''
