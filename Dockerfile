FROM nvidia/cuda:8.0-cudnn6-devel
LABEL maintainer="Ming <i@ufoym.com>"

# =================================
# cuda          8.0
# cudnn         v6
# ---------------------------------
# python        3.5
# opencv        latest (git)
# ---------------------------------
# tensorflow    latest (pip)
# sonnet        latest (pip)
# pytorch       0.2.0  (pip)
# keras         latest (pip)
# mxnet         latest (pip)
# cntk          2.2    (pip)
# chainer       latest (pip)
# theano        latest (git)
# lasagne       latest (git)
# caffe         latest (git)
# torch         latest (git)
# ---------------------------------

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="pip --no-cache-dir install --upgrade" && \
    GIT_CLONE="git clone --depth 10" && \

# =================================
# apt
# =================================

    rm -rf /var/lib/apt/lists/* \
           /etc/apt/sources.list.d/cuda.list \
           /etc/apt/sources.list.d/nvidia-ml.list && \

    apt-get update && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        apt-utils \
        && \

# =================================
# common tools
# =================================

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        build-essential \
        ca-certificates \
        wget \
        git \
        vim \
        && \

# =================================
# cmake
# =================================

    # fix boost-not-found issue caused by the `apt-get` version of cmake
    $GIT_CLONE https://github.com/Kitware/CMake ~/cmake && \
    cd ~/cmake && \
    ./bootstrap --prefix=/usr/local && \
    make -j"$(nproc)" install && \

# =================================
# python3
# =================================

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        python3-pip \
        python3-dev \
        && \
    ln -s /usr/bin/python3 /usr/local/bin/python && \
    pip3 --no-cache-dir install --upgrade pip && \
    $PIP_INSTALL \
        setuptools \
        numpy \
        scipy \
        pandas \
        scikit-learn \
        matplotlib \
        Cython \
        && \

# =================================
# opencv
# =================================

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        && \

    $GIT_CLONE https://github.com/opencv/opencv ~/opencv && \
    mkdir -p ~/opencv/build && cd ~/opencv/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D WITH_IPP=OFF \
          -D WITH_CUDA=OFF \
          -D WITH_OPENCL=OFF \
          -D BUILD_TESTS=OFF \
          -D BUILD_PERF_TESTS=OFF \
          .. && \
    make -j"$(nproc)" install && \

# =================================
# tensorflow
# =================================

    $PIP_INSTALL \
        tensorflow_gpu \
        && \

# =================================
# sonnet
# =================================

    $PIP_INSTALL \
        dm-sonnet \
        && \

# =================================
# mxnet
# =================================

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        graphviz \
        && \

    $PIP_INSTALL \
        mxnet-cu80 \
        graphviz \
        && \

# =================================
# cntk
# =================================

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        openmpi-bin \
        libjasper-dev \
        && \

    $PIP_INSTALL \
        https://cntk.ai/PythonWheel/GPU/cntk-2.2-cp35-cp35m-linux_x86_64.whl \
        && \

# =================================
# keras
# =================================

    $PIP_INSTALL \
        h5py \
        keras \
        && \

# =================================
# pytorch
# =================================

    $PIP_INSTALL \
        http://download.pytorch.org/whl/cu80/torch-0.2.0.post3-cp35-cp35m-manylinux1_x86_64.whl \
        torchvision \
        && \

# =================================
# chainer
# =================================

    $PIP_INSTALL \
        cupy \
        chainer \
        && \

# =================================
# theano
# =================================

    $GIT_CLONE https://github.com/Theano/Theano ~/theano && \
    cd ~/theano && \
    $PIP_INSTALL \
        . && \

    $GIT_CLONE https://github.com/Theano/libgpuarray ~/gpuarray && \
    mkdir -p ~/gpuarray/build && cd ~/gpuarray/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          .. && \
    make -j"$(nproc)" install && \
    cd ~/gpuarray && \
    python setup.py build && \
    python setup.py install && \

    printf '[global]\nfloatX = float32\ndevice = cuda0\n\n[dnn]\ninclude_path = /usr/local/cuda/targets/x86_64-linux/include\n' \
    > ~/.theanorc && \

# =================================
# lasagne
# =================================

    $GIT_CLONE https://github.com/Lasagne/Lasagne ~/lasagne && \
    cd ~/lasagne && \
    $PIP_INSTALL \
        . && \

# =================================
# caffe
# =================================

    $GIT_CLONE https://github.com/NVIDIA/nccl && \
    cd nccl; make -j"$(nproc)" install; cd ..; rm -rf nccl && \

    $GIT_CLONE https://github.com/BVLC/caffe ~/caffe && \
    mkdir ~/caffe/build && cd ~/caffe/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D USE_CUDNN=1 \
          -D USE_NCCL=1 \
          -D python_version=3 \
          -D CUDA_NVCC_FLAGS=--Wno-deprecated-gpu-targets \
          -Wno-dev \
          .. && \
    make -j"$(nproc)" install && \

    # fix ValueError caused by python-dateutil 1.x
    sed -i 's/,<2//g' ~/caffe/python/requirements.txt && \

    $PIP_INSTALL \
        -r ~/caffe/python/requirements.txt && \

    mv /usr/local/python/caffe /usr/local/lib/python3.5/dist-packages/ && \
    rm -rf /usr/local/python && \

# =================================
# torch
# =================================

    $GIT_CLONE https://github.com/torch/distro.git ~/torch --recursive&& \

    cd ~/torch/exe/luajit-rocks && \
    mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D WITH_LUAJIT21=ON \
          .. && \
    make -j"$(nproc)" install && \

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        libreadline-dev \
        && \

    $GIT_CLONE https://github.com/Yonaba/Moses ~/moses && \
    cd ~/moses && \
    luarocks install rockspec/moses-1.6.1-1.rockspec && \

    cd ~/torch && \
    sed -i 's/extra\/cudnn/extra\/cudnn \&\& git checkout R6/' install.sh && \
    sed -i 's/$PREFIX\/bin\/luarocks/luarocks/' install.sh && \
    sed -i '/qt/d' install.sh && \
    sed -i '/Installing Lua/,/^cd \.\.$/d' install.sh && \
    sed -i '/path_to_nvidiasmi/,/^fi$/d' install.sh && \
    sed -i '/Restore anaconda/,/^Not updating$/d' install.sh && \
    sed -i '/You might want to/,/^fi$/d' install.sh && \
    yes no | ./install.sh && \


# =================================
# config & cleanup
# =================================

    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/*  ~/*
