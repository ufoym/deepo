# -*- coding: utf-8 -*-

"""Generate dockerfiles & CI configuration."""

import os
import textwrap


def indent(n, s):
    prefix = ' ' * 4 * n
    return ''.join(prefix + l for l in s.splitlines(True))


def get_tags(postfix,
    default_mod='all',
    default_platform='cu101',
    default_pyver='py36'):

    terms = postfix.split('-')
    if len(terms) == 2:
        mod, platform = terms
        pyver = None
    else:
        mod = '-'.join(terms[:-2])
        pyver, platform = terms[-2], terms[-1]

    tags = [postfix]
    if platform == default_platform:
        tags.append('-'.join(filter(None, (mod, pyver))))
    if pyver == default_pyver:
        tags.append('-'.join(filter(None, (mod, platform))))
    if mod == default_mod:
        tags.append('-'.join(filter(None, (pyver, platform))))
    if platform == default_platform and pyver == default_pyver:
        tags.append(mod)
    if mod == default_mod and pyver == default_pyver:
        tags.append(platform)
    if mod == default_mod and platform == default_platform:
        tags.append(pyver)
        if platform == default_platform:
            tags.append('latest')

    if mod == 'all':
        for t in list(tags):
            tags.append(t.replace('all', 'all-jupyter'))

    return tags


def get_job(tags):
    job_name = '_'.join(tags)
    build_scripts = indent(1, textwrap.dedent('''
        "%s":
            machine: true
            steps:
                - checkout
                - run:
                    command: docker build %s -f docker/Dockerfile.%s .
                    no_output_timeout: 1h
                - run: docker login -u $DOCKER_USER -p $DOCKER_PASS''' % (
                    job_name,
                    ' '.join('-t $DOCKER_REPO:%s' % tag for tag in tags),
                    tags[0])))
    is_all = False
    for tag in tags:
        build_scripts += indent(3, textwrap.dedent('''
            - run: docker push $DOCKER_REPO:%s''' % tag))
        if 'all' in tag:
            is_all = True
    if is_all:
        test_scripts = textwrap.dedent('''
            import tensorflow as m; print(m.__name__, ':', m.__version__);
            import sonnet as m; print(m.__name__, ':', m.__version__);
            import torch as m; print(m.__name__, ':', m.__version__);
            import keras as m; print(m.__name__, ':', m.__version__);
            import mxnet as m; print(m.__name__, ':', m.__version__);
            import cntk as m; print(m.__name__, ':', m.__version__);
            import chainer as m; print(m.__name__, ':', m.__version__);
            import theano as m; print(m.__name__, ':', m.__version__);
            import lasagne as m; print(m.__name__, ':', m.__version__);
            import caffe as m; print(m.__name__, ':', m.__version__);
            import caffe2.python as m; dir(m); print(m.__name__, ':', m.__version__);
            ''').replace('\n', '')
        run_prefix = '- run: docker run $DOCKER_REPO:%s ' % tags[0]
        build_scripts += indent(3, textwrap.dedent('''
            %s python -c "%s"
            %s caffe --version
            %s darknet
            %s th
            ''' % (run_prefix, test_scripts,
                   run_prefix, run_prefix, run_prefix)))

    build_scripts += '\n'
    return job_name, build_scripts


def generate(ci_fname):
    with open(ci_fname, 'w') as f:
        f.write(textwrap.dedent('''
            version: 2.0
            jobs:
        ''')[1:])

    job_names = []
    for fn in os.listdir(os.path.join('..', 'docker')):
        postfix = fn.split('.')[-1]
        tags = get_tags(postfix)
        job_name, build_scripts = get_job(tags)
        job_names.append(job_name)

        with open(ci_fname, 'a') as f:
            f.write(build_scripts)

    workflow_scripts = textwrap.dedent('''

        workflows:
            version: 2
            build:
                jobs:
    ''')[1:]
    workflow_scripts += indent(
        3, '\n'.join('- "%s"' % job_name for job_name in job_names))
    with open(ci_fname, 'a') as f:
        f.write(workflow_scripts)


if __name__ == '__main__':
    generate('../circle.yml')
