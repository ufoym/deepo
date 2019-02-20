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

            cd ~/torch && \
            rm -fr cmake/3.6/Modules/FindCUDA* && \
            patch -p0 <<'EOF'
            diff --git a/lib/THC/THCAtomics.cuh b/lib/THC/THCAtomics.cuh
            index 400875c..ccb7a1c 100644
            --- a/lib/THC/THCAtomics.cuh
            +++ b/lib/THC/THCAtomics.cuh
            @@ -94,6 +94,7 @@ static inline __device__ void atomicAdd(long *address, long val) {
             }

             #ifdef CUDA_HALF_TENSOR
            +#if !(__CUDA_ARCH__ >= 700 || !defined(__CUDA_ARCH__) )
             static inline  __device__ void atomicAdd(half *address, half val) {
               unsigned int * address_as_ui =
                   (unsigned int *) ((char *)address - ((size_t)address & 2));
            @@ -117,6 +118,7 @@ static inline  __device__ void atomicAdd(half *address, half val) {
                } while (assumed != old);
             }
             #endif
            +#endif
            EOF && \

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
            luarocks install image && \
            luarocks install nn && \
        '''
