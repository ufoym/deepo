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


def get_command(modules, postfix, cpu_only):
    if cpu_only:
        postfix += '-cpu'
    return 'python ../generator/generate.py ../docker/Dockerfile.%s %s%s\n' % (
        postfix,
        ' '.join(m for m in modules),
        ' --cpu-only' if cpu_only else ''
    )


def generate(f, cpu_only):

        # single module
        for module in candidate_modules:
            if module in non_cpu_only_modules and cpu_only:
                continue
            elif module in non_python_modules:
                modules = [module]
                f.write(get_command(modules, module, cpu_only))
            else:
                for pyver in pyvers:
                    modules = [module, 'python==%s' % pyver]
                    postfix = '%s-py%s' % (
                        module, pyver.replace('.', ''))
                    f.write(get_command(modules, postfix, cpu_only))

        # all modules
        for pyver in pyvers:
            modules = candidate_modules + ['python==%s' % pyver]
            postfix = 'all-py%s' % pyver.replace('.', '')
            f.write(get_command(modules, postfix, cpu_only))

        # all modules with jupyter
        for pyver in pyvers:
            modules = candidate_modules + ['python==%s' % pyver, 'jupyter']
            postfix = 'all-py%s-jupyter' % pyver.replace('.', '')
            f.write(get_command(modules, postfix, cpu_only))


if __name__ == '__main__':
    with open('gen-docker.sh', 'w') as f:
        generate(f, cpu_only=False)
        generate(f, cpu_only=True)
