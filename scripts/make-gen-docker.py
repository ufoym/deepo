# -*- coding: utf-8 -*-

"""Generate scripts for generating dockerfiles."""

candidate_modules = [
    'tensorflow',
    'mxnet',
    'keras',
    'pytorch',
    'chainer',
    'darknet',
    'paddle',
    # 'caffe',
    # 'theano',
    # 'lasagne',
    # 'cntk',
    # 'sonnet',
    # 'torch',
]

non_python_modules = [
    'torch',
    'darknet',
]

deprecated_modules = {
    'torch': ('10.2', '7'),
}

pyvers = [
    # '2.7',
    # '3.6',
    '3.8',
]


def get_command(modules, postfix, cuda_ver, cudnn_ver):
    cuver = 'cpu' if cuda_ver is None else 'cu%s' % ''.join(cuda_ver.split('.')[:2])
    postfix += '-%s' % cuver
    return 'python ../generator/generate.py ../docker/Dockerfile.%s %s%s%s\n' % (
        postfix,
        ' '.join(m for m in modules),
        '' if cuda_ver is None else ' --cuda-ver %s' % cuda_ver,
        '' if cudnn_ver is None else ' --cudnn-ver %s' % cudnn_ver,
    )


def generate(f, cuda_ver=None, cudnn_ver=None):

        # single module
        for module in candidate_modules:
            _cuda_ver, _cudnn_ver = cuda_ver, cudnn_ver
            if None not in (cuda_ver, cudnn_ver):   # with cuda
                if module in deprecated_modules:
                    _cuda_ver, _cudnn_ver = deprecated_modules[module]
            if module in non_python_modules:
                modules = [module]
                f.write(get_command(modules, module, _cuda_ver, _cudnn_ver))
            else:
                for pyver in pyvers:
                    modules = [module, 'python==%s' % pyver]
                    postfix = '%s-py%s' % (
                        module, pyver.replace('.', ''))
                    f.write(get_command(modules, postfix, _cuda_ver, _cudnn_ver))

        # all modules
        for pyver in pyvers:
            modules = list(candidate_modules)
            if None not in (cuda_ver, cudnn_ver):   # with cuda
                modules = [m for m in modules if m not in deprecated_modules]
            modules += ['python==%s' % pyver, 'onnx', 'jupyterlab']
            postfix = 'all-py%s' % pyver.replace('.', '')
            f.write(get_command(modules, postfix, cuda_ver, cudnn_ver))


if __name__ == '__main__':
    with open('gen-docker.sh', 'w') as f:
        generate(f)
        # generate(f, '8.0', '6')
        # generate(f, '9.0', '7')
        # generate(f, '10.1', '7')
        # generate(f, '10.2', '7')
        # generate(f, '11.1', '8')
        generate(f, '11.3.1', '8')
