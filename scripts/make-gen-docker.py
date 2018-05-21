# -*- coding: utf-8 -*-

"""Generate scripts for generating dockerfiles."""

candidate_modules = [
    'tensorflow',
    'sonnet',
    'mxnet',
    'cntk',
    'keras',
    'pytorch',
    'chainer',
    'theano',
    'lasagne',
    'caffe',
    'caffe2',
    'torch',
]

non_python_modules = [
    'torch',
]

non_cpu_only_modules = [
    'pytorch',
]

pyvers = [
    '2.7',
    # '3.5',
    '3.6',
]


def get_command(modules, postfix, cuda_ver, cudnn_ver):
    cuver = 'cpu' if cuda_ver is None else 'cu%d' % (float(cuda_ver) * 10)
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
            if module in non_cpu_only_modules and cuda_ver is None:
                continue
            elif module in non_python_modules:
                modules = [module]
                f.write(get_command(modules, module, cuda_ver, cudnn_ver))
            else:
                for pyver in pyvers:
                    modules = [module, 'python==%s' % pyver]
                    postfix = '%s-py%s' % (
                        module, pyver.replace('.', ''))
                    f.write(get_command(modules, postfix, cuda_ver, cudnn_ver))

        # all modules
        for pyver in pyvers:
            modules = candidate_modules + ['python==%s' % pyver]
            postfix = 'all-py%s' % pyver.replace('.', '')
            f.write(get_command(modules, postfix, cuda_ver, cudnn_ver))

        # all modules with jupyter
        for pyver in pyvers:
            modules = candidate_modules + ['python==%s' % pyver, 'jupyter']
            postfix = 'all-jupyter-py%s' % pyver.replace('.', '')
            f.write(get_command(modules, postfix, cuda_ver, cudnn_ver))


if __name__ == '__main__':
    with open('gen-docker.sh', 'w') as f:
        generate(f)
        # generate(f, '8.0', '6')
        generate(f, '9.0', '7')
