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
    'torch',
]

non_python_modules = [
    'torch',
]

pyvers = [
    '2.7',
    # '3.5',
    '3.6',
]


def get_command(modules, postfix):
    return 'python ../generator/generate.py ../docker/Dockerfile.%s %s\n' % (
        postfix, ' '.join(m for m in modules))


def generate(script_path):

    with open(script_path, 'w') as f:

        # single module
        for module in candidate_modules:
            if module in non_python_modules:
                modules = [module]
                f.write(get_command(modules, module))
            else:
                for pyver in pyvers:
                    modules = [module, 'python==%s' % pyver]
                    postfix = '%s-py%s' % (
                        module, pyver.replace('.', ''))
                    f.write(get_command(modules, postfix))

        # all modules
        for pyver in pyvers:
            modules = candidate_modules + ['python==%s' % pyver]
            postfix = 'all-py%s' % pyver.replace('.', '')
            f.write(get_command(modules, postfix))

        # all modules with jupyter
        for pyver in pyvers:
            modules = candidate_modules + ['python==%s' % pyver, 'jupyter']
            postfix = 'all-py%s-jupyter' % pyver.replace('.', '')
            f.write(get_command(modules, postfix))


if __name__ == '__main__':
    generate('gen-docker.sh')
