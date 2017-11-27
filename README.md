![deepo](https://user-images.githubusercontent.com/2270240/32102393-aecf573c-bb4e-11e7-811c-dc673cae7b9c.png)

[![CircleCI](https://img.shields.io/circleci/project/github/ufoym/deepo.svg)](https://circleci.com/gh/ufoym/deepo)
[![docker](https://img.shields.io/docker/pulls/ufoym/deepo.svg)](https://hub.docker.com/r/ufoym/deepo)
![license](https://img.shields.io/github/license/ufoym/deepo.svg)


***Deepo*** is a series of [*Docker*](http://www.docker.com/) images that
- allows you to quickly set up your deep learning research environment
- supports almost all commonly used deep learning frameworks: [theano](http://deeplearning.net/software/theano), [tensorflow](http://www.tensorflow.org), [sonnet](https://github.com/deepmind/sonnet), [pytorch](http://pytorch.org), [keras](https://keras.io), [lasagne](http://lasagne.readthedocs.io), [mxnet](http://mxnet.incubator.apache.org), [cntk](https://www.microsoft.com/en-us/cognitive-toolkit), [chainer](https://chainer.org), [caffe](http://caffe.berkeleyvision.org), [torch](http://torch.ch/)

and their Dockerfile generator that
- allows you to customize your own environment with Lego-like modules
- automatically resolves the dependencies for you


# Table of contents
- [Quick Start](#Quick-Start)
  - [Installation](#Installation)
  - [Usage](#Usage)
- [Customization](#Customization)
  - [I hate all-in-one solution](#One)
  - [Other python versions](#Python)
  - [Build your own customized image](#Build)
- [Comparison to Alternatives](#Comparison)
- [Contributing](#Contributing)
- [Licensing](#Licensing)

---

<a name="Quick-Start"/>

# Quick Start


<a name="Installation"/>

## Installation

#### Step 1. Install [Docker](https://docs.docker.com/engine/installation/) and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker).

#### Step 2. Obtain the all-in-one image from [Docker Hub](https://hub.docker.com/r/ufoym/deepo)

```bash
docker pull ufoym/deepo
```

<a name="Usage"/>

## Usage

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

## I hate all-in-one solution

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

See [https://hub.docker.com/r/ufoym/deepo/tags/](https://hub.docker.com/r/ufoym/deepo/tags/) for a complete list of all available tags. These pre-built images are all built from `docker/Dockerfile.*` and `circle.yml`. See [How to generate `docker/Dockerfile.*` and `circle.yml`](https://github.com/ufoym/deepo/tree/master/scripts) if you are interested in how these files are generated.

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
 [cuda](https://developer.nvidia.com/cuda-zone)    | :x:                  | 8.0                | 6.5-8.0              | 8.0
 [cudnn](https://developer.nvidia.com/cudnn)       | :x:                  | v5                 | v2-5                 | v6
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
 [torch](http://torch.ch/)                         | :x:                  | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark:


<a name="Contributing"/>

# Contributing

We appreciate all contributions. If you are planning to contribute back bug-fixes, please do so without any further discussion. If you plan to contribute new features, utility functions or extensions, please first open an issue and discuss the feature with us.

<a name="Licensing"/>

# Licensing

Deepo is [MIT licensed](https://github.com/ufoym/deepo/blob/master/LICENSE).
