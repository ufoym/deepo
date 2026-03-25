![deepo](https://user-images.githubusercontent.com/2270240/32102393-aecf573c-bb4e-11e7-811c-dc673cae7b9c.png)

![workflows](https://github.com/ufoym/deepo/workflows/deepo%20CI/badge.svg)
[![docker](https://img.shields.io/docker/pulls/ufoym/deepo.svg)](https://hub.docker.com/r/ufoym/deepo)
![license](https://img.shields.io/github/license/ufoym/deepo.svg)


---

***Deepo*** is an open framework for painlessly assembling specialized [*Docker*](http://www.docker.com/) images for deep learning research. It provides a "Lego set" of dozens of standard components for preparing deep learning tools, along with a framework for composing them into custom Docker images.

At the core of Deepo is a Dockerfile generator that
- lets you [customize your deep learning environment](#Build) with Lego-like modules
  - describe your environment in a single command line
  - Deepo generates Dockerfiles following best practices
  - and handles all the configuration for you
- automatically resolves dependencies
  - Deepo knows which combinations of CUDA, cuDNN, Python, PyTorch, TensorFlow, etc. are compatible
  - picks the right versions on your behalf
  - and determines the correct installation order via [topological sorting](https://en.wikipedia.org/wiki/Topological_sorting)

We also provide a series of pre-built Docker images that
- let you instantly set up common deep learning research environments
- support widely used [deep learning frameworks](#Available-tags)
- support [GPU acceleration](#GPU) (CUDA and cuDNN included) and also work in [CPU-only mode](#CPU)
- run on Linux ([CPU](#CPU)/[GPU](#GPU)), Windows ([CPU](#CPU)), and macOS ([CPU](#CPU))

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

#### Step 1. Install [Docker](https://docs.docker.com/engine/installation/) and [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

#### Step 2. Pull the all-in-one image from [Docker Hub](https://hub.docker.com/r/ufoym/deepo)

```bash
docker pull ufoym/deepo
```

<a name="Usage"/>

### Usage

Verify that GPU access works inside a container:
```bash
docker run --gpus all --rm ufoym/deepo nvidia-smi
```
If this does not work, check [the issues section of the NVIDIA Container Toolkit GitHub](https://github.com/NVIDIA/nvidia-container-toolkit/issues) — many solutions are already documented. To launch an interactive shell in a persistent container:

```bash
docker run --gpus all -it ufoym/deepo bash
```

To share data and configuration between the host (your machine or VM) and the container, use the `-v` option:
```bash
docker run --gpus all -it -v /host/data:/data -v /host/config:/config ufoym/deepo bash
```
This makes `/host/data` on the host visible as `/data` inside the container, and `/host/config` as `/config`. This isolation helps prevent containerized experiments from accidentally overwriting or reading the wrong data.

Note that some frameworks (e.g., PyTorch) use shared memory for inter-process communication. If you use multiprocessing, the container's default shared memory size may be insufficient. Increase it with `--ipc=host` or `--shm-size`:
```bash
docker run --gpus all -it --ipc=host ufoym/deepo bash
```


<a name="CPU"/>

## CPU Version

<a name="Installation-cpu"/>

### Installation

#### Step 1. Install [Docker](https://docs.docker.com/engine/installation/).

#### Step 2. Pull the all-in-one image from [Docker Hub](https://hub.docker.com/r/ufoym/deepo)

```bash
docker pull ufoym/deepo:cpu
```

<a name="Usage-cpu"/>

### Usage

Launch an interactive shell:
```bash
docker run -it ufoym/deepo:cpu bash
```

To share data and configuration between the host (your machine or VM) and the container, use the `-v` option:
```bash
docker run -it -v /host/data:/data -v /host/config:/config ufoym/deepo:cpu bash
```
This makes `/host/data` on the host visible as `/data` inside the container, and `/host/config` as `/config`. This isolation helps prevent containerized experiments from accidentally overwriting or reading the wrong data.

Note that some frameworks (e.g., PyTorch) use shared memory for inter-process communication. If you use multiprocessing, the container's default shared memory size may be insufficient. Increase it with `--ipc=host` or `--shm-size`:
```bash
docker run -it --ipc=host ufoym/deepo:cpu bash
```


_You are now ready to begin your journey._


```
$ python
```
```python
>>> import tensorflow
>>> import torch
>>> import keras
>>> import mxnet
>>> import chainer
>>> import paddle
```

```
$ darknet
```
```
usage: darknet <function>
```

<a name="Customization"/>

# Customization

The `docker pull ufoym/deepo` command from [Quick Start](#Quick-Start) gives you a standard image containing every available deep learning framework. You can also customize your own environment.

<a name="One"/>

## Unhappy with all-in-one solution?

If you prefer a single framework instead of the all-in-one image, simply append a tag with the framework name.
For example, to pull TensorFlow only:
```bash
docker pull ufoym/deepo:tensorflow
```

<a name="Jupyter"/>

## Jupyter Support

#### Step 1. Pull the all-in-one image

```bash
docker pull ufoym/deepo
```

#### Step 2. Run the image
```bash
docker run --gpus all -it -p 8888:8888 -v /home/u:/root --ipc=host ufoym/deepo jupyter lab --no-browser --ip=0.0.0.0 --allow-root --LabApp.allow_origin='*' --LabApp.root_dir='/root'
```


<a name="Build"/>

## Build Your Own Customized Image with Lego-like Modules

#### Step 1. Set up the generator

```bash
git clone https://github.com/ufoym/deepo.git
cd deepo/generator
```

#### Step 2. Generate a customized Dockerfile

For example, to create an image with `pytorch` and `keras`:
```bash
python generate.py Dockerfile pytorch keras
```
Or with CUDA 11.3 and cuDNN 8:
```bash
python generate.py Dockerfile pytorch keras --cuda-ver 11.3.1 --cudnn-ver 8
```

This generates a Dockerfile with everything needed to build `pytorch` and `keras`. The generator automatically resolves dependencies and topologically sorts them, so you don't need to worry about missing packages or ordering.

You can also specify the Python version:
```bash
python generate.py Dockerfile pytorch keras python==3.8
```

#### Step 3. Build the Dockerfile

```bash
docker build -t my/deepo .
```

This may take several minutes, as some libraries are compiled from source.


<a name="Comparison"/>

# Comparison to Alternatives


.                                                  | modern-deep-learning | dl-docker          | jupyter-deeplearning | Deepo
:------------------------------------------------: | :------------------: | :----------------: | :------------------: | :----------------:
 [ubuntu](https://www.ubuntu.com)                  | 16.04                | 14.04              | 14.04                | 20.04
 [cuda](https://developer.nvidia.com/cuda-zone)    | X                    | 8.0                | 6.5-8.0              | 11.3/None
 [cudnn](https://developer.nvidia.com/cudnn)       | X                    | v5                 | v2-5                 | v8
 [onnx](https://onnx.ai)                           | X                    | X                  | X                    | O
 [tensorflow](http://www.tensorflow.org)            | O                    | O                  | O                    | O
 [pytorch](http://pytorch.org)                      | X                    | X                  | X                    | O
 [keras](https://keras.io)                          | O                    | O                  | O                    | O
 [mxnet](http://mxnet.incubator.apache.org)         | X                    | X                  | X                    | O
 [chainer](https://chainer.org)                     | X                    | X                  | X                    | O
 [darknet](https://pjreddie.com/darknet/)           | X                    | X                  | X                    | O
 [paddlepaddle](https://www.paddlepaddle.org.cn/)   | X                    | X                  | X                    | O



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
 [PaddlePaddle](https://www.paddlepaddle.org.cn/)  | `paddle-cu113` `paddle`                                   | `paddle-cpu`


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
    title = {Deepo: Set up a deep learning environment with a single command line.},
    year = {2017},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/ufoym/deepo}}
}
```
<a name="Contributing"/>

# Contributing

We appreciate all contributions. If you are planning to contribute bug fixes, please go ahead and open a pull request directly. If you plan to contribute new features, utility functions, or extensions, please open an issue first to discuss your idea with us.

<a name="Licensing"/>

# Licensing

Deepo is [MIT licensed](https://github.com/ufoym/deepo/blob/master/LICENSE).
