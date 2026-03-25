# -*- coding: utf-8 -*-
import textwrap
import functools


class Composer:

    def __init__(self, modules, cuda_ver, cudnn_ver, ubuntu_ver, versions=None):
        if versions is None:
            versions = {}
        if not modules:
            raise ValueError('Modules should contain at least one module')
        pending = self._traverse(modules)
        self.modules = list(self._toposort(pending))
        self.instances = self._get_instances(versions)
        self.cuda_ver = cuda_ver
        self.cudnn_ver = cudnn_ver
        self.ubuntu_ver = ubuntu_ver

    def get(self):
        return self.modules

    def ver(self, module):
        for ins in self.instances:
            if ins.__class__ is module:
                return ins.version
        return None

    def to_dockerfile(self):
        def _indent(n, s):
            prefix = ' ' * 4 * n
            return ''.join(prefix + line for line in s.splitlines(True))

        if self.cuda_ver is None:
            base_image = f'ubuntu:{self.ubuntu_ver}'
        else:
            cudnn_part = f'-cudnn{self.cudnn_ver}' if self.cudnn_ver else ''
            base_image = f'nvidia/cuda:{self.cuda_ver}{cudnn_part}-devel-ubuntu{self.ubuntu_ver}'

        ports = ' '.join(str(p) for m in self.instances for p in m.expose())
        return textwrap.dedent(''.join([
            _indent(3, ''.join([
                self._split('module list'),
                ''.join(f'# {repr(m)}\n'
                    for m in self.instances if repr(m)),
                self._split(),
            ])),
            r'''
            FROM %s
            ENV LANG C.UTF-8
            RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
                PIP_INSTALL="python -m pip --no-cache-dir install --upgrade" && \
                GIT_CLONE="git clone --depth 10" && \

                rm -rf /var/lib/apt/lists/* \
                       /etc/apt/sources.list.d/cuda.list \
                       /etc/apt/sources.list.d/nvidia-ml.list && \

                apt-get update && \
            ''' % base_image,
            '\n',
            '\n'.join([
                ''.join([
                    _indent(3, self._split(m.name())),
                    _indent(1, m.build()),
                ]) for m in self.instances
            ]),
            '\n',
            _indent(3, self._split('config & cleanup')),
            r'''
                ldconfig && \
                apt-get clean && \
                apt-get autoremove && \
                rm -rf /var/lib/apt/lists/* /tmp/* ~/*
            ''',
            f'''
            EXPOSE {ports}
            ''' if ports else '',
            ]))

    def _traverse(self, modules):
        seen = set(modules)
        current_level = modules
        while current_level:
            next_level = []
            for module in current_level:
                yield module
                for child in module.deps:
                    if child not in seen:
                        next_level.append(child)
                        seen.add(child)
            current_level = next_level

    def _toposort(self, pending):
        data = {m: set(m.deps) for m in pending}
        for v in data.values():
            v.discard(v)
        extra_items_in_deps = functools.reduce(
            set.union, data.values()) - set(data.keys())
        data.update({item: set() for item in extra_items_in_deps})
        while True:
            ordered = {item for item, dep in data.items() if not dep}
            if not ordered:
                break
            for m in sorted(ordered, key=lambda m: m.__name__):
                yield m
            data = {
                item: (dep - ordered)
                for item, dep in data.items()
                if item not in ordered
            }
        if data:
            raise ValueError(
                'Circular dependencies exist among these items: '
                '{{{}}}'.format(', '.join(
                    f'{key!r}:{value!r}' for key, value in sorted(
                        data.items()))))

    def _split(self, title=None):
        split_l = '# ' + '=' * 66 + '\n'
        split_s = '# ' + '-' * 66 + '\n'
        if title is None:
            return split_l
        return split_l + f'# {title}\n' + split_s

    def _get_instances(self, versions):
        instances = []
        for m in self.modules:
            ins = m(self)
            if m in versions:
                ins.version = versions[m]
            instances.append(ins)
        return instances
