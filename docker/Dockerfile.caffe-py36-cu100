# ==================================================================
# module list
# ------------------------------------------------------------------
# python        3.6    (apt)
# opencv        4.0.1  (git)
# caffe         latest (git)
# ==================================================================

FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
ENV LANG C.UTF-8
RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    PIP_INSTALL="python -m pip --no-cache-dir install --upgrade" && \
    GIT_CLONE="git clone --depth 10" && \

    rm -rf /var/lib/apt/lists/* \
           /etc/apt/sources.list.d/cuda.list \
           /etc/apt/sources.list.d/nvidia-ml.list && \

    apt-get update && \

# ==================================================================
# tools
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        build-essential \
        apt-utils \
        ca-certificates \
        wget \
        git \
        vim \
        && \

    $GIT_CLONE https://github.com/Kitware/CMake ~/cmake && \
    cd ~/cmake && \
    ./bootstrap && \
    make -j"$(nproc)" install && \

# ==================================================================
# python
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        software-properties-common \
        && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        python3.6 \
        python3.6-dev \
        python3-distutils-extra \
        && \
    wget -O ~/get-pip.py \
        https://bootstrap.pypa.io/get-pip.py && \
    python3.6 ~/get-pip.py && \
    ln -s /usr/bin/python3.6 /usr/local/bin/python3 && \
    ln -s /usr/bin/python3.6 /usr/local/bin/python && \
    $PIP_INSTALL \
        setuptools \
        && \
    $PIP_INSTALL \
        numpy \
        scipy \
        pandas \
        cloudpickle \
        scikit-learn \
        matplotlib \
        Cython \
        && \

# ==================================================================
# boost
# ------------------------------------------------------------------

    wget -O ~/boost.tar.gz https://dl.bintray.com/boostorg/release/1.69.0/source/boost_1_69_0.tar.gz && \
    tar -zxf ~/boost.tar.gz -C ~ && \
    cd ~/boost_* && \
    ./bootstrap.sh --with-python=python3.6 && \
    ./b2 install -j"$(nproc)" --prefix=/usr/local && \

# ==================================================================
# opencv
# ------------------------------------------------------------------

    DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
        libatlas-base-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        && \

    $GIT_CLONE --branch 4.0.1 https://github.com/opencv/opencv ~/opencv && \
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
    ln -s /usr/local/include/opencv4/opencv2 /usr/local/include/opencv2 && \

# ==================================================================
# caffe
# ------------------------------------------------------------------

    $GIT_CLONE https://github.com/BVLC/caffe ~/caffe && \
    sed -i 's/CV_LOAD_IMAGE_COLOR/cv::IMREAD_COLOR/g' ~/caffe/src/caffe/layers/window_data_layer.cpp && \
    sed -i 's/CV_LOAD_IMAGE_COLOR/cv::IMREAD_COLOR/g' ~/caffe/src/caffe/util/io.cpp && \
    sed -i 's/CV_LOAD_IMAGE_GRAYSCALE/cv::IMREAD_GRAYSCALE/g' ~/caffe/src/caffe/util/io.cpp && \
    cp ~/caffe/Makefile.config.example ~/caffe/Makefile.config && \
    sed -i 's/# USE_CUDNN/USE_CUDNN/g' ~/caffe/Makefile.config && \
    sed -i 's/# PYTHON_LIBRARIES/PYTHON_LIBRARIES/g' ~/caffe/Makefile.config && \
    sed -i 's/# WITH_PYTHON_LAYER/WITH_PYTHON_LAYER/g' ~/caffe/Makefile.config && \
    sed -i 's/# OPENCV_VERSION/OPENCV_VERSION/g' ~/caffe/Makefile.config && \
    sed -i 's/# USE_NCCL/USE_NCCL/g' ~/caffe/Makefile.config && \
    sed -i 's/-gencode arch=compute_20,code=sm_20//g' ~/caffe/Makefile.config && \
    sed -i 's/-gencode arch=compute_20,code=sm_21//g' ~/caffe/Makefile.config && \
    sed -i 's/2\.7/3\.6/g' ~/caffe/Makefile.config && \
    sed -i 's/3\.5/3\.6/g' ~/caffe/Makefile.config && \
    sed -i 's/boost_python3/boost_python36/g' ~/caffe/Makefile.config && \
    sed -i 's/\/usr\/lib\/python/\/usr\/local\/lib\/python/g' ~/caffe/Makefile.config && \
    sed -i 's/\/usr\/local\/include/\/usr\/local\/include \/usr\/include\/hdf5\/serial/g' ~/caffe/Makefile.config && \
    sed -i 's/hdf5/hdf5_serial/g' ~/caffe/Makefile && \
    sed -i 's/# Debugging/COMMON_FLAGS += -std=c++11\n# Debugging/g' ~/caffe/Makefile && \
    cd ~/caffe && \
    make -j"$(nproc)" -Wno-deprecated-gpu-targets distribute && \

    # fix ValueError caused by python-dateutil 1.x
    sed -i 's/,<2//g' ~/caffe/python/requirements.txt && \

    $PIP_INSTALL \
        -r ~/caffe/python/requirements.txt && \

    cd ~/caffe/distribute/bin && \
    for file in *.bin; do mv "$file" "${file%%.bin}"; done && \
    cd ~/caffe/distribute && \
    cp -r bin include lib proto /usr/local/ && \
    cp -r python/caffe /usr/local/lib/python3.6/dist-packages/ && \

# ==================================================================
# config & cleanup
# ------------------------------------------------------------------

    ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*
