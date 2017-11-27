# -*- coding: utf-8 -*-

"""Top-level package for genv."""

__author__ = """Ming"""
__email__ = 'i@ufoym.com'
__version__ = '0.1.1'

from .core.manager import Manager

from .modules.tools import Tools
from .modules.python import Python
from .modules.boost import Boost
from .modules.opencv import Opencv

from .modules.tensorflow import Tensorflow
from .modules.sonnet import Sonnet
from .modules.mxnet import Mxnet
from .modules.cntk import Cntk
from .modules.keras import Keras
from .modules.pytorch import Pytorch
from .modules.chainer import Chainer
from .modules.theano import Theano
from .modules.lasagne import Lasagne
from .modules.caffe import Caffe
from .modules.torch import Torch

__all__ = [
    'Manager', 'Tools', 'Python', 'Boost', 'Opencv',
    'Tensorflow', 'Sonnet', 'Mxnet', 'Cntk', 'Keras',
    'Pytorch', 'Chainer', 'Theano', 'Lasagne', 'Caffe',
    'Torch',
]
