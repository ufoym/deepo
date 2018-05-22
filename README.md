![deepo](https://user-images.githubusercontent.com/2270240/32102393-aecf573c-bb4e-11e7-811c-dc673cae7b9c.png)

[![CircleCI](https://img.shields.io/circleci/project/github/ufoym/deepo.svg)](https://circleci.com/gh/ufoym/deepo)
[![docker](https://img.shields.io/docker/pulls/ufoym/deepo.svg)](https://hub.docker.com/r/ufoym/deepo)
![license](https://img.shields.io/github/license/ufoym/deepo.svg)


***Deepo*** is a series of [*Docker*](http://www.docker.com/) images that
- allows you to quickly set up your deep learning research environment
- supports almost all [commonly used deep learning frameworks](#tags)
- supports [GPU acceleration](#GPU) (CUDA and cuDNN included), also works in [CPU-only mode](#CPU)
- works on Linux ([CPU version](#CPU)/[GPU version](#GPU)), Windows ([CPU version](#CPU)) and OS X ([CPU version](#CPU))

and their Dockerfile generator that
- allows you to [customize your own environment](#Build) with Lego-like modules
- automatically resolves the dependencies for you

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
  - [Other python versions](#Python)
  - [Jupyter support](#Jupyter)
  - [Build your own customized image](#Build)
- [Comparison to Alternatives](#Comparison)
- [Available Tags](#tags)
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

<a name="Usage"/>

### Usage

Now you can try this command:
```bash
nvidia-docker run --rm ufoym/deepo nvidia-smi
```
This should work and enables Deepo to use the GPU from inside a docker container.
If this does not work, search [the issues section on the nvidia-docker GitHub](https://github.com/NVIDIA/nvidia-docker/issues) -- many solutions are already documented. To get an interactive shell to a container that will not be automatically deleted after you exit do

```bash
nvidia-docker run -it ufoym/deepo bash
```

If you want to share your data and configurations between the host (your machine or VM) and the container in which you are using Deepo, use the -v option, e.g.
```bash
nvidia-docker run -it -v /host/data:/data -v /host/config:/config ufoym/deepo bash
```
This will make `/host/data` from the host visible as `/data` in the container, and `/host/config` as `/config`. Such isolation reduces the chances of your containerized experiments overwriting or using wrong data.

Please note that some frameworks (e.g. PyTorch) use shared memory to share data between processes, so if multiprocessing is used the default shared memory segment size that container runs with is not enough, and you should increase shared memory size either with `--ipc=host` or `--shm-size` command line options to `nvidia-docker run`.
```bash
nvidia-docker run -it --ipc=host ufoym/deepo bash
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
>>> import caffe2
```

```$ caffe --version```
```
caffe version 1.0.0
```

```$ th```
```
 │  ______             __   |  Torch7
 │ /_  __/__  ________/ /   |  Scientific computing for Lua.
 │  / / / _ \/ __/ __/ _ \  |  Type ? for help
 │ /_/  \___/_/  \__/_//_/  |  https://github.com/torch
 │                          |  http://torch.ch
 │
 │th>
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

<a name="Python"/>

## Other python versions

Note that all python-related images use `Python 3.6` by default. If you are unhappy with `Python 3.6`, you can also specify other python versions:
```bash
docker pull ufoym/deepo:py27
```

```bash
docker pull ufoym/deepo:tensorflow-py27
```

Currently, we support `Python 2.7` and `Python 3.6`.

See [Available Tags](#tags) for a complete list of all available tags. These pre-built images are all built from `docker/Dockerfile.*` and `circle.yml`. See [How to generate `docker/Dockerfile.*` and `circle.yml`](https://github.com/ufoym/deepo/tree/master/scripts) if you are interested in how these files are generated.

<a name="Jupyter"/>

## Jupyter support

#### Step 1. pull the image with jupyter support

```bash
docker pull ufoym/deepo:all-py36-jupyter
```

Note that the tag could be either of `all-py36-jupyter`, `py36-jupyter`, `all-py27-jupyter`, or `py27-jupyter`.

#### Step 2. run the image
```bash
nvidia-docker run -it -p 8888:8888 --ipc=host ufoym/deepo:all-jupyter-py36 jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/root'
```


<a name="Build"/>

## Build your own customized image with Lego-like modules

#### Step 1. prepare generator

```bash
git clone https://github.com/ufoym/deepo.git
cd deepo/generator
pip install -r requirements.txt
```

#### Step 2. generate your customized Dockerfile

For example, if you like `pytorch` and `lasagne`, then
```bash
python generate.py Dockerfile pytorch lasagne
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
 [ubuntu](https://www.ubuntu.com)                  | 16.04                | 14.04              | 14.04                | 16.04
 [cuda](https://developer.nvidia.com/cuda-zone)    | :x:                  | 8.0                | 6.5-8.0              | 8.0/9.0/None
 [cudnn](https://developer.nvidia.com/cudnn)       | :x:                  | v5                 | v2-5                 | v7
 [theano](http://deeplearning.net/software/theano) | :x:                  | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark:
 [tensorflow](http://www.tensorflow.org)           | :heavy_check_mark:   | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark:
 [sonnet](https://github.com/deepmind/sonnet)      | :x:                  | :x:                | :x:                  | :heavy_check_mark:
 [pytorch](http://pytorch.org)                     | :x:                  | :x:                | :x:                  | :heavy_check_mark:
 [keras](https://keras.io)                         | :heavy_check_mark:   | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark:
 [lasagne](http://lasagne.readthedocs.io)          | :x:                  | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark:
 [mxnet](http://mxnet.incubator.apache.org)        | :x:                  | :x:                | :x:                  | :heavy_check_mark:
 [cntk](http://cntk.ai)                            | :x:                  | :x:                | :x:                  | :heavy_check_mark:
 [chainer](https://chainer.org)                    | :x:                  | :x:                | :x:                  | :heavy_check_mark:
 [caffe](http://caffe.berkeleyvision.org)          | :heavy_check_mark:   | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark:
 [caffe2](https://caffe2.ai)                        | :x:                  | :x:                | :x:                  | :heavy_check_mark:
 [torch](http://torch.ch/)                         | :x:                  | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark:



---

<a name="tags"/>

# Available Tags


.                                                  | CUDA 9.0 / Python 3.6                                    | CUDA 9.0 / Python 2.7                    | CPU-only / Python 3.6                       | CPU-only / Python 2.7
:------------------------------------------------: | :------------------------------------------------------: | :--------------------------------:       | :-----------------------------------------: | :----------------------------------------:
 all-in-one                                        | `latest` `all` `all-py36` `py36-cu90` `all-py36-cu90`    | `all-py27-cu90` `all-py27` `py27`        | `all-py36-cpu` `all-cpu` `py36-cpu` `cpu`   | `all-py27-cpu` `py27-cpu`
 all-in-one with jupyter                           | `all-jupyter-py36-cu90` `all-jupyter-py36` `all-jupyter` | `all-py27-jupyter` `py27-jupyter`        | `all-py36-jupyter-cpu` `py36-jupyter-cpu`   | `all-py27-jupyter-cpu` `py27-jupyter-cpu`
 [theano](http://deeplearning.net/software/theano) | `theano-py36-cu90` `theano-py36` `theano`                | `theano-py27-cu90` `theano-py27`         | `theano-py36-cpu` `theano-cpu`              | `theano-py27-cpu`
 [tensorflow](http://www.tensorflow.org)           | `tensorflow-py36-cu90` `tensorflow-py36` `tensorflow`    | `tensorflow-py27-cu90` `tensorflow-py27` | `tensorflow-py36-cpu` `tensorflow-cpu`      | `tensorflow-py27-cpu`
 [sonnet](https://github.com/deepmind/sonnet)      | `sonnet-py36-cu90` `sonnet-py36` `sonnet`                | `sonnet-py27-cu90` `sonnet-py27`         | `sonnet-py36-cpu` `sonnet-cpu`              | `sonnet-py27-cpu`
 [pytorch](http://pytorch.org)                     | `pytorch-py36-cu90` `pytorch-py36` `pytorch`             | `pytorch-py27-cu90` `pytorch-py27`       | `pytorch-py36` `pytorch`                    | `pytorch-py27`
 [keras](https://keras.io)                         | `keras-py36-cu90` `keras-py36` `keras`                   | `keras-py27-cu90` `keras-py27`           | `keras-py36-cpu` `keras-cpu`                | `keras-py27-cpu`
 [lasagne](http://lasagne.readthedocs.io)          | `lasagne-py36-cu90` `lasagne-py36` `lasagne`             | `lasagne-py27-cu90` `lasagne-py27`       | `lasagne-py36-cpu` `lasagne-cpu`            | `lasagne-py27-cpu`
 [mxnet](http://mxnet.incubator.apache.org)        | `mxnet-py36-cu90` `mxnet-py36` `mxnet`                   | `mxnet-py27-cu90` `mxnet-py27`           | `mxnet-py36-cpu` `mxnet-cpu`                | `mxnet-py27-cpu`
 [cntk](http://cntk.ai)                            | `cntk-py36-cu90` `cntk-py36` `cntk`                      | `cntk-py27-cu90` `cntk-py27`             | `cntk-py36-cpu` `cntk-cpu`                  | `cntk-py27-cpu`
 [chainer](https://chainer.org)                    | `chainer-py36-cu90` `chainer-py36` `chainer`             | `chainer-py27-cu90` `chainer-py27`       | `chainer-py36-cpu` `chainer-cpu`            | `chainer-py27-cpu`
 [caffe](http://caffe.berkeleyvision.org)          | `caffe-py36-cu90` `caffe-py36` `caffe`                   | `caffe-py27-cu90` `caffe-py27`           | `caffe-py36-cpu` `caffe-cpu`                | `caffe-py27-cpu`
 [caffe2](https://caffe2.ai)                       | `caffe2-py36-cu90` `caffe2-py36` `caffe2`                | `caffe2-py27-cu90` `caffe2-py27`         | `caffe2-py36-cpu` `caffe2-cpu`              | `caffe2-py27-cpu`
 [torch](http://torch.ch/)                         | `torch-cu90` `torch`                                     | `torch-cu90` `torch`                     | `torch-cpu`                                 | `torch-cpu`

---



<a name="Contributing"/>

# Contributing

We appreciate all contributions. If you are planning to contribute back bug-fixes, please do so without any further discussion. If you plan to contribute new features, utility functions or extensions, please first open an issue and discuss the feature with us.

<a name="Licensing"/>

# Licensing

Deepo is [MIT licensed](https://github.com/ufoym/deepo/blob/master/LICENSE).
