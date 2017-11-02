![deepo](https://user-images.githubusercontent.com/2270240/32102393-aecf573c-bb4e-11e7-811c-dc673cae7b9c.png)

[![CircleCI](https://img.shields.io/circleci/project/github/ufoym/deepo.svg)](https://circleci.com/gh/ufoym/deepo)
![license](https://img.shields.io/github/license/ufoym/deepo.svg)

*Available in: [English](README.md), [简体中文](README_zh-CN.md)*

Docker镜像打包了所有流行的深度学习框架。一方面，它为深度学习开发提供了方便，可以直接使用Deepo镜像，而不用自行搭建环境。另一方面，Deepo提供了一个统一的环境，为重现深度学习研究结果提供了便利。

Deepo包含以下深度学习框架：

- [theano](http://deeplearning.net/software/theano)
- [tensorflow](http://www.tensorflow.org)
- [sonnet](https://github.com/deepmind/sonnet)
- [pytorch](http://pytorch.org)
- [keras](https://keras.io)
- [lasagne](http://lasagne.readthedocs.io)
- [mxnet](http://mxnet.incubator.apache.org)
- [cntk](https://www.microsoft.com/en-us/cognitive-toolkit)
- [chainer](https://chainer.org)
- [caffe](http://caffe.berkeleyvision.org)
- [torch](http://torch.ch/)

#### 快速开始

首先安装[Docker](https://docs.docker.com/engine/installation/)和[nvidia-docker](https://github.com/NVIDIA/nvidia-docker)。

从Docker Hub拉取镜像：

```bash
docker pull ufoym/deepo
```

运行：

```bash
nvidia-docker run --rm ufoym/deepo nvidia-smi
```

交互式运行（退出后不会自动销毁）：

```bash
nvidia-docker run -it ufoym/deepo bash
```

和主机共享配置和数据：

```bash
nvidia-docker run -it -v /host/data:/data -v /host/config:/config ufoym/deepo bash
```

目录的对应关系：

| 主机 | 容器 |
| -- | -- |
| `/host/data` | `/data` |
| `/host/config` | `/config` |

#### 查看包含的框架的版本（路径）

```python
>>> import tensorflow
>>> print(tensorflow.__name__, tensorflow.__version__)
tensorflow 1.3.0

>>> import sonnet
>>> print(sonnet.__name__, sonnet.__path__)
sonnet ['/usr/local/lib/python3.5/dist-packages/sonnet']

>>> import torch
>>> print(torch.__name__, torch.__version__)
torch 0.2.0_3

>>> import keras
>>> print(keras.__name__, keras.__version__)
keras 2.0.8

>>> import mxnet
>>> print(mxnet.__name__, mxnet.__version__)
mxnet 0.11.0

>>> import cntk
>>> print(cntk.__name__, cntk.__version__)
cntk 2.2

>>> import chainer
>>> print(chainer.__name__, chainer.__version__)
chainer 3.0.0

>>> import theano
>>> print(theano.__name__, theano.__version__)
theano 0.10.0beta4+14.gb6e3768

>>> import lasagne
>>> print(lasagne.__name__, lasagne.__version__)
lasagne 0.2.dev1

>>> import caffe
>>> print(caffe.__name__, caffe.__version__)
caffe 1.0.0
```

```sh
; th
 │  ______             __   |  Torch7
 │ /_  __/__  ________/ /   |  Scientific computing for Lua.
 │  / / / _ \/ __/ __/ _ \  |  Type ? for help
 │ /_/  \___/_/  \__/_//_/  |  https://github.com/torch
 │                          |  http://torch.ch
 │
 │th>
```

#### 与同类项目的比较

.      | modern-deep-learning | dl-docker          | jupyter-deeplearning | Deepo
:------------------------------------------------: | :------------------: | :----------------: | :------------------: | :----------------:
 [ubuntu](https://www.ubuntu.com)                  | 16.04                | 14.04              | 14.04                | 16.04
 [cuda](https://developer.nvidia.com/cuda-zone)    | ❌                  | 8.0                | 6.5-8.0              | 8.0
 [cudnn](https://developer.nvidia.com/cudnn)       | ❌                  | v5                 | v2-5                 | v6
 [theano](http://deeplearning.net/software/theano) | ❌                  | ✔️ | ✔️   | ✔️
 [tensorflow](http://www.tensorflow.org)           | ✔️   | ✔️ | ✔️   | ✔️
 [sonnet](https://github.com/deepmind/sonnet)      | ❌                  | ❌                | ❌                  | ✔️
 [pytorch](http://pytorch.org)                     | ❌                  | ❌                | ❌                  | ✔️
 [keras](https://keras.io)                         | ✔️   | ✔️ | ✔️   | ✔️
 [lasagne](http://lasagne.readthedocs.io)          | ❌                  | ✔️ | ✔️   | ✔️
 [mxnet](http://mxnet.incubator.apache.org)        | ❌                  | ❌                | ❌                  | ✔️
 [cntk](http://cntk.ai)                            | ❌                  | ❌                | ❌                  | ✔️
 [chainer](https://chainer.org)                    | ❌                  | ❌                | ❌                  | ✔️
 [caffe](http://caffe.berkeleyvision.org)          | ✔️   | ✔️ | ✔️   | ✔️
 [torch](http://torch.ch/)                         | ❌                  | ✔️️ | ✔️   | ✔️

#### 许可

[MIT](https://github.com/ufoym/deepo/blob/master/LICENSE)

*中文翻译：[@论智](https://mp.weixin.qq.com/s/aK1Ry5R6tMTn6z6llEGxHQ)*