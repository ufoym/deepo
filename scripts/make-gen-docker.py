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
]

non_python_modules = [
    'torch',
    'darknet',
]

deprecated_modules = {
    'torch': ('10.2', '7'),
}

pyvers = [
    '3.8',
]


def get_command(modules, postfix, cuda_ver, cudnn_ver):
    cuver = 'cpu' if cuda_ver is None else f"cu{''.join(cuda_ver.split('.')[:2])}"
    postfix += f'-{cuver}'
    modules_str = ' '.join(modules)
    cuda_opt = '' if cuda_ver is None else f' --cuda-ver {cuda_ver}'
    cudnn_opt = '' if cudnn_ver is None else f' --cudnn-ver {cudnn_ver}'
    return f'python ../generator/generate.py ../docker/Dockerfile.{postfix} {modules_str}{cuda_opt}{cudnn_opt}\n'


def generate(f, cuda_ver=None, cudnn_ver=None):

        for module in candidate_modules:
            _cuda_ver, _cudnn_ver = cuda_ver, cudnn_ver
            if None not in (cuda_ver, cudnn_ver):
                if module in deprecated_modules:
                    _cuda_ver, _cudnn_ver = deprecated_modules[module]
            if module in non_python_modules:
                modules = [module]
                f.write(get_command(modules, module, _cuda_ver, _cudnn_ver))
            else:
                for pyver in pyvers:
                    modules = [module, f'python=={pyver}']
                    postfix = f"{module}-py{pyver.replace('.', '')}"
                    f.write(get_command(modules, postfix, _cuda_ver, _cudnn_ver))

        for pyver in pyvers:
            modules = list(candidate_modules)
            if None not in (cuda_ver, cudnn_ver):
                modules = [m for m in modules if m not in deprecated_modules]
            modules += [f'python=={pyver}', 'onnx', 'jupyterlab']
            postfix = f"all-py{pyver.replace('.', '')}"
            f.write(get_command(modules, postfix, cuda_ver, cudnn_ver))


if __name__ == '__main__':
    with open('gen-docker.sh', 'w') as f:
        generate(f)
        generate(f, '11.3.1', '8')
