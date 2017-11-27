# -*- coding: utf-8 -*-

"""Console script for generator."""

import os
import sys
import click

from core.composer import Composer

from modules.tools import Tools
from modules.python import Python
from modules.boost import Boost
from modules.opencv import Opencv

from modules.tensorflow import Tensorflow
from modules.sonnet import Sonnet
from modules.mxnet import Mxnet
from modules.cntk import Cntk
from modules.keras import Keras
from modules.pytorch import Pytorch
from modules.chainer import Chainer
from modules.theano import Theano
from modules.lasagne import Lasagne
from modules.caffe import Caffe
from modules.torch import Torch


@click.command()
@click.argument('path', nargs=1)
@click.argument('modules', nargs=-1)
def main(path, modules):
    """
    Generate a dockerfile according to the given modules to be installed.
    """
    in_modules = []
    versions = {}
    for module in modules:
        terms = module.split('==')
        m = getattr(sys.modules[__name__], terms[0].title())
        in_modules.append(m)
        if len(terms) > 1:
            versions[m] = terms[1]
    composer = Composer(in_modules, versions)
    with open(path, 'w') as f:
        f.write(composer.to_dockerfile())


if __name__ == "__main__":
    main()
