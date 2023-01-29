![deepo](https://user-images.githubusercontent.com/2270240/32102393-aecf573c-bb4e-11e7-811c-dc673cae7b9c.png)

![workflows](https://github.com/ufoym/deepo/workflows/deepo%20CI/badge.svg)
[![docker](https://img.shields.io/docker/pulls/ufoym/deepo.svg)](https://hub.docker.com/r/ufoym/deepo)
![build](https://img.shields.io/docker/automated/ufoym/deepo.svg)
![license](https://img.shields.io/github/license/ufoym/deepo.svg)


***PLEASE NOTE, THE DEEP LEARNING FRAMEWORK WAR IS OVER, THIS PROJECT IS NO LONGER BEING MAINTAINED.***

---

***Deepo*** is an open framework to assemble specialized [*docker*](http://www.docker.com/) images for deep learning research without pain. It provides a “lego set” of dozens of standard components for preparing deep learning tools and a framework for assembling them into custom docker images. 

At the core of Deepo is a Dockerfile generator that
- allows you to [customize your deep learning environment](#Build) with Lego-like modules
  - define your environment in a single command line,
  - then deepo will generate Dockerfiles with best practices
  - and do all the configuration for you
- automatically resolves the dependencies for you
  - deepo knows which combos (CUDA/cuDNN/Python/PyTorch/Tensorflow, ..., tons of dependancies) are compatible
  - and will pick the right versions for you
  - and arrange sequence of installation procedures using [topological sorting](https://en.wikipedia.org/wiki/Topological_sorting)

We also prepare a series of pre-built docker images that
- allows you to instantly set up common deep learning research environment
- supports almost all [commonly used deep learning frameworks](#Available-tags)
- supports [GPU acceleration](#GPU) (CUDA and cuDNN included), also works in [CPU-only mode](#CPU)
- works on Linux ([CPU version](#CPU)/[GPU version](#GPU)), Windows ([CPU version](#CPU)) and OS X ([CPU version](#CPU))

---

# Table of contents
- [Quick Start](#Quick-Start)
  - [GPU Version](#GPU)
    - [Installation](#Installation)
    - [Usage](#Usage)
  - [CPU Version](#CPU)
    - [Installation](#Installation-cpu)
    - [Usage](#Usage-cpu)
- [Customization](#Customization)
  - [Unhappy with all-in-one solution?](#One)
  - [Jupyter support](#Jupyter)
  - [Build your own customized image](#Build)
- [Comparison to Alternatives](#Comparison)
- [Tags](#Tags)
  - [Available Tags](#Available-tags)
  - [Deprecated Tags](#Deprecated-tags)
- [Citation](#Citation)
- [Contributing](#Contributing)
- [Licensing](#Licensing)

---

<a name="Quick-Start"/>

# Quick Start


<a name="GPU"/>

## GPU Version

<a name="Installation"/>

### Installation

#### Step 1. Install [Docker](https://docs.docker.com/engine/installation/) and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker).

#### Step 2. Obtain the all-in-one image from [Docker Hub](https://hub.docker.com/r/ufoym/deepo)

```bash
docker pull ufoym/deepo
```

For users in China who may suffer from slow speeds when pulling the image from the public Docker registry, you can pull `deepo` images from the China registry mirror by specifying the full path, including the registry, in your docker pull command, for example:

```bash
docker pull registry.docker-cn.com/ufoym/deepo
```

<a name="Usage"/>

### Usage

Now you can try this command:
```bash
docker run --gpus all --rm ufoym/deepo nvidia-smi
```
This should work and enables Deepo to use the GPU from inside a docker container.
If this does not work, search [the issues section on the nvidia-docker GitHub](https://github.com/NVIDIA/nvidia-docker/issues) -- many solutions are already documented. To get an interactive shell to a container that will not be automatically deleted after you exit do

```bash
docker run --gpus all -it ufoym/deepo bash
```

If you want to share your data and configurations between the host (your machine or VM) and the container in which you are using Deepo, use the -v option, e.g.
```bash
docker run --gpus all -it -v /host/data:/data -v /host/config:/config ufoym/deepo bash
```
This will make `/host/data` from the host visible as `/data` in the container, and `/host/config` as `/config`. Such isolation reduces the chances of your containerized experiments overwriting or using wrong data.

Please note that some frameworks (e.g. PyTorch) use shared memory to share data between processes, so if multiprocessing is used the default shared memory segment size that container runs with is not enough, and you should increase shared memory size either with `--ipc=host` or `--shm-size` command line options to `docker run`.
```bash
docker run --gpus all -it --ipc=host ufoym/deepo bash
```


<a name="CPU"/>

## CPU Version

<a name="Installation-cpu"/>

### Installation

#### Step 1. Install [Docker](https://docs.docker.com/engine/installation/).

#### Step 2. Obtain the all-in-one image from [Docker Hub](https://hub.docker.com/r/ufoym/deepo)

```bash
docker pull ufoym/deepo:cpu
```

<a name="Usage-cpu"/>

### Usage

Now you can try this command:
```bash
docker run -it ufoym/deepo:cpu bash
```

If you want to share your data and configurations between the host (your machine or VM) and the container in which you are using Deepo, use the -v option, e.g.
```bash
docker run -it -v /host/data:/data -v /host/config:/config ufoym/deepo:cpu bash
```
This will make `/host/data` from the host visible as `/data` in the container, and `/host/config` as `/config`. Such isolation reduces the chances of your containerized experiments overwriting or using wrong data.

Please note that some frameworks (e.g. PyTorch) use shared memory to share data between processes, so if multiprocessing is used the default shared memory segment size that container runs with is not enough, and you should increase shared memory size either with `--ipc=host` or `--shm-size` command line options to `docker run`.
```bash
docker run -it --ipc=host ufoym/deepo:cpu bash
```


_You are now ready to begin your journey._


```$ python```
```python
>>> import tensorflow
>>> import sonnet
>>> import torch
>>> import keras
>>> import mxnet
>>> import cntk
>>> import chainer
>>> import theano
>>> import lasagne
>>> import caffe
>>> import paddle
```

```$ caffe --version```
```
caffe version 1.0.0
```

```$ darknet```
```
usage: darknet <function>
```

<a name="Customization"/>

# Customization

Note that `docker pull ufoym/deepo` mentioned in [Quick Start](#Quick-Start) will give you a standard image containing all available deep learning frameworks. You can customize your own environment as well.

<a name="One"/>

## Unhappy with all-in-one solution?

If you prefer a specific framework rather than an all-in-one image, just append a tag with the name of the framework.
Take tensorflow for example:
```bash
docker pull ufoym/deepo:tensorflow
```

<a name="Jupyter"/>

## Jupyter support

#### Step 1. pull the all-in-one image

```bash
docker pull ufoym/deepo
```

#### Step 2. run the image
```bash
docker run --gpus all -it -p 8888:8888 -v /home/u:/root --ipc=host ufoym/deepo jupyter lab --no-browser --ip=0.0.0.0 --allow-root --LabApp.allow_origin='*' --LabApp.root_dir='/root'
```


<a name="Build"/>

## Build your own customized image with Lego-like modules

#### Step 1. prepare generator

```bash
git clone https://github.com/ufoym/deepo.git
cd deepo/generator
```

#### Step 2. generate your customized Dockerfile

For example, if you like `pytorch` and `lasagne`, then
```bash
python generate.py Dockerfile pytorch lasagne
```
or with CUDA 11.1 and CUDNN 8
```bash
python generate.py Dockerfile pytorch lasagne --cuda-ver 11.1 --cudnn-ver 8
```

This should generate a Dockerfile that contains everything for building `pytorch` and `lasagne`. Note that the generator can handle automatic dependency processing and topologically sort the lists. So you don't need to worry about missing dependencies and the list order.

You can also specify the version of Python:
```bash
python generate.py Dockerfile pytorch lasagne python==3.6
```

#### Step 3. build your Dockerfile

```bash
docker build -t my/deepo .
```

This may take several minutes as it compiles a few libraries from scratch.


<a name="Comparison"/>

# Comparison to alternatives


.                                                  | modern-deep-learning | dl-docker          | jupyter-deeplearning | Deepo
:------------------------------------------------: | :------------------: | :----------------: | :------------------: | :----------------:
 [ubuntu](https://www.ubuntu.com)                  | 16.04                | 14.04              | 14.04                | 18.04
 [cuda](https://developer.nvidia.com/cuda-zone)    | X                    | 8.0                | 6.5-8.0              | 8.0-10.2/None
 [cudnn](https://developer.nvidia.com/cudnn)       | X                    | v5                 | v2-5                 | v7
 [onnx](https://onnx.ai)                           | X                    | X                  | X                    | O
 [theano](http://deeplearning.net/software/theano) | X                    | O                  | O                    | O
 [tensorflow](http://www.tensorflow.org)           | O                    | O                  | O                    | O
 [sonnet](https://github.com/deepmind/sonnet)      | X                    | X                  | X                    | O
 [pytorch](http://pytorch.org)                     | X                    | X                  | X                    | O
 [keras](https://keras.io)                         | O                    | O                  | O                    | O
 [lasagne](http://lasagne.readthedocs.io)          | X                    | O                  | O                    | O
 [mxnet](http://mxnet.incubator.apache.org)        | X                    | X                  | X                    | O
 [cntk](http://cntk.ai)                            | X                    | X                  | X                    | O
 [chainer](https://chainer.org)                    | X                    | X                  | X                    | O
 [caffe](http://caffe.berkeleyvision.org)          | O                    | O                  | O                    | O
 [caffe2](https://caffe2.ai)                       | X                    | X                  | X                    | O
 [torch](http://torch.ch/)                         | X                    | O                  | O                    | O
 [darknet](https://pjreddie.com/darknet/)          | X                    | X                  | X                    | O
 [paddlepaddle](https://www.paddlepaddle.org.cn/)  | X                    | X                  | X                    | O



<a name="Tags"/>

# Tags


<a name="Available-tags"/>

## Available Tags


.                                                  | CUDA 11.3 / Python 3.8                                    | CPU-only / Python 3.8
:------------------------------------------------: | :-------------------------------------------------------: | :-----------------------------------------:
 all-in-one                                        | `latest` `all` `all-py38` `py38-cu113` `all-py38-cu113`   | `all-py38-cpu` `all-cpu` `py38-cpu` `cpu`
 [TensorFlow](http://www.tensorflow.org)           | `tensorflow-py38-cu113` `tensorflow-py38` `tensorflow`    | `tensorflow-py38-cpu` `tensorflow-cpu`
 [PyTorch](http://pytorch.org)                     | `pytorch-py38-cu113` `pytorch-py38` `pytorch`             | `pytorch-py38-cpu` `pytorch-cpu`
 [Keras](https://keras.io)                         | `keras-py38-cu113` `keras-py38` `keras`                   | `keras-py38-cpu` `keras-cpu`
 [MXNet](http://mxnet.incubator.apache.org)        | `mxnet-py38-cu113` `mxnet-py38` `mxnet`                   | `mxnet-py38-cpu` `mxnet-cpu`
 [Chainer](https://chainer.org)                    | `chainer-py38-cu113` `chainer-py38` `chainer`             | `chainer-py38-cpu` `chainer-cpu`
 [Darknet](https://pjreddie.com/darknet/)          | `darknet-cu113` `darknet`                                 | `darknet-cpu`
 [paddlepaddle](https://www.paddlepaddle.org.cn/)  | `paddle-cu113` `paddle`                                   | `paddle-cpu`


<a name="Deprecated-tags"/>

## Deprecated Tags

.                                                  | CUDA 11.3 / Python 3.6         | CUDA 11.1 / Python 3.6         | CUDA 10.1 / Python 3.6         | CUDA 10.0 / Python 3.6         | CUDA 9.0 / Python 3.6                        | CUDA 9.0 / Python 2.7                    | CPU-only / Python 3.6                       | CPU-only / Python 2.7
:------------------------------------------------: | :----------------------------: | :----------------------------: | :----------------------------: | :----------------------------: | :------------------------------------------: | :--------------------------------:       | :-----------------------------------------: | :----------------------------------------:
 all-in-one                                        | `py36-cu113` `all-py36-cu113`  | `py36-cu111` `all-py36-cu111`  | `py36-cu101` `all-py36-cu101`  | `py36-cu100` `all-py36-cu100`  | `py36-cu90` `all-py36-cu90`                  | `all-py27-cu90` `all-py27` `py27-cu90`   |                                             | `all-py27-cpu` `py27-cpu`
 all-in-one with jupyter                           |                                |                                |                                |                                | `all-jupyter-py36-cu90`                      | `all-py27-jupyter` `py27-jupyter`        |                                             | `all-py27-jupyter-cpu` `py27-jupyter-cpu`
 [Theano](http://deeplearning.net/software/theano) | `theano-py36-cu113`            | `theano-py36-cu111`            | `theano-py36-cu101`            | `theano-py36-cu100`            | `theano-py36-cu90`                           | `theano-py27-cu90` `theano-py27`         |                                             | `theano-py27-cpu`
 [TensorFlow](http://www.tensorflow.org)           | `tensorflow-py36-cu113`        | `tensorflow-py36-cu111`        | `tensorflow-py36-cu101`        | `tensorflow-py36-cu100`        | `tensorflow-py36-cu90`                       | `tensorflow-py27-cu90` `tensorflow-py27` |                                             | `tensorflow-py27-cpu`
 [Sonnet](https://github.com/deepmind/sonnet)      | `sonnet-py36-cu113`            | `sonnet-py36-cu111`            | `sonnet-py36-cu101`            | `sonnet-py36-cu100`            | `sonnet-py36-cu90`                           | `sonnet-py27-cu90` `sonnet-py27`         |                                             | `sonnet-py27-cpu`
 [PyTorch](http://pytorch.org)                     | `pytorch-py36-cu113`           | `pytorch-py36-cu111`           | `pytorch-py36-cu101`           | `pytorch-py36-cu100`           | `pytorch-py36-cu90`                          | `pytorch-py27-cu90` `pytorch-py27`       |                                             | `pytorch-py27-cpu`
 [Keras](https://keras.io)                         | `keras-py36-cu113`             | `keras-py36-cu111`             | `keras-py36-cu101`             | `keras-py36-cu100`             | `keras-py36-cu90`                            | `keras-py27-cu90` `keras-py27`           |                                             | `keras-py27-cpu`
 [Lasagne](http://lasagne.readthedocs.io)          | `lasagne-py36-cu113`           | `lasagne-py36-cu111`           | `lasagne-py36-cu101`           | `lasagne-py36-cu100`           | `lasagne-py36-cu90`                          | `lasagne-py27-cu90` `lasagne-py27`       |                                             | `lasagne-py27-cpu`
 [MXNet](http://mxnet.incubator.apache.org)        | `mxnet-py36-cu113`             | `mxnet-py36-cu111`             | `mxnet-py36-cu101`             | `mxnet-py36-cu100`             | `mxnet-py36-cu90`                            | `mxnet-py27-cu90` `mxnet-py27`           |                                             | `mxnet-py27-cpu`
 [CNTK](http://cntk.ai)                            | `cntk-py36-cu113`              | `cntk-py36-cu111`              | `cntk-py36-cu101`              | `cntk-py36-cu100`              | `cntk-py36-cu90`                             | `cntk-py27-cu90` `cntk-py27`             |                                             | `cntk-py27-cpu`
 [Chainer](https://chainer.org)                    | `chainer-py36-cu113`           | `chainer-py36-cu111`           | `chainer-py36-cu101`           | `chainer-py36-cu100`           | `chainer-py36-cu90`                          | `chainer-py27-cu90` `chainer-py27`       |                                             | `chainer-py27-cpu`
 [Caffe](http://caffe.berkeleyvision.org)          | `caffe-py36-cu113`             | `caffe-py36-cu111`             | `caffe-py36-cu101`             | `caffe-py36-cu100`             | `caffe-py36-cu90`                            | `caffe-py27-cu90` `caffe-py27`           |                                             | `caffe-py27-cpu`
 [Caffe2](https://caffe2.ai)                       |                                |                                |                                |                                | `caffe2-py36-cu90` `caffe2-py36` `caffe2`    | `caffe2-py27-cu90` `caffe2-py27`         | `caffe2-py36-cpu` `caffe2-cpu`              | `caffe2-py27-cpu`
 [Torch](http://torch.ch/)                         | `torch-cu113`                  | `torch-cu111`                  | `torch-cu101`                  | `torch-cu100`                  | `torch-cu90`                                 | `torch-cu90` `torch`                     |                                             | `torch-cpu`
 [Darknet](https://pjreddie.com/darknet/)          | `darknet-cu113`                | `darknet-cu111`                | `darknet-cu101`                | `darknet-cu100`                | `darknet-cu90`                               | `darknet-cu90` `darknet`                 |                                             | `darknet-cpu`


<a name="Citation"/>

# Citation
```
@misc{ming2017deepo,
    author = {Ming Yang},
    title = {Deepo: set up deep learning environment in a single command line.},
    year = {2017},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/ufoym/deepo}}
}
```
<a name="Contributing"/>

# Contributing

We appreciate all contributions. If you are planning to contribute back bug-fixes, please do so without any further discussion. If you plan to contribute new features, utility functions or extensions, please first open an issue and discuss the feature with us.

<a name="Licensing"/>

# Licensing

Deepo is [MIT licensed](https://github.com/ufoym/deepo/blob/master/LICENSE).
