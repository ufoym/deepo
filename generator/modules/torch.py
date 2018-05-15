# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source
from .tools import Tools


@dependency(Tools)
@source('git')
class Torch(Module):

    def build(self):
        return r'''
            export TORCH_NVCC_FLAGS="-D__CUDA_NO_HALF_OPERATORS__" && \
            $GIT_CLONE https://github.com/torch/distro.git ~/torch''' \
        + r''' --recursive && \

            cd ~/torch/exe/luajit-rocks && \
            mkdir build && cd build && \
            cmake -D CMAKE_BUILD_TYPE=RELEASE \
                  -D CMAKE_INSTALL_PREFIX=/usr/local \
                  -D WITH_LUAJIT21=ON \
                  .. && \
            make -j"$(nproc)" install && \

            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                libjpeg-dev \
                libpng-dev \
                libreadline-dev \
                && \

            $GIT_CLONE https://github.com/Yonaba/Moses ~/moses && \
            cd ~/moses && \
            luarocks install rockspec/moses-1.6.1-1.rockspec && \

            cd ~/torch && \
            sed -i 's/extra\/cudnn/extra\/cudnn ''' \
        + r'''\&\& git checkout R7/' install.sh && \
            sed -i 's/$PREFIX\/bin\/luarocks/luarocks/' install.sh && \
            sed -i '/qt/d' install.sh && \
            sed -i '/Installing Lua/,/^cd \.\.$/d' install.sh && \
            sed -i '/path_to_nvidiasmi/,/^fi$/d' install.sh && \
            sed -i '/Restore anaconda/,/^Not updating$/d' install.sh && \
            sed -i '/You might want to/,/^fi$/d' install.sh && \
            '''.rstrip() + (r'''
            sed -i 's/\[ -x "$path_to_nvcc" \]/false/' install.sh && \
            '''.rstrip() if self.composer.cuda_ver is None else ''
        ) + r'''
            yes no | ./install.sh && \
        '''
