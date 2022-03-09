# -*- coding: utf-8 -*-

"""Generate dockerfiles & CI configuration."""

import os
import textwrap


def indent(n, s):
    prefix = ' ' * 4 * n
    return ''.join(prefix + l for l in s.splitlines(True))


def get_tags(postfix,
    default_mod='all',
    default_platform='cu',
    default_lang='py'):

    def is_default_mod(mod):
        return mod and default_mod in mod
    def is_default_platform(platform):
        return platform and default_platform in platform
    def is_default_lang(lang):
        return lang and default_lang in lang

    terms = postfix.split('-')
    if len(terms) == 2:
        mod, platform = terms
        pyver = None
    else:
        mod = '-'.join(terms[:-2])
        pyver, platform = terms[-2], terms[-1]

    tags = [postfix]
    if is_default_platform(platform):
        tags.append('-'.join(filter(None, (mod, pyver))))
    if is_default_lang(pyver):
        tags.append('-'.join(filter(None, (mod, platform))))
    if is_default_mod(mod):
        tags.append('-'.join(filter(None, (pyver, platform))))
    if is_default_platform(platform) and is_default_lang(pyver):
        tags.append(mod)
    if is_default_mod(mod) and is_default_lang(pyver):
        tags.append(platform)
    if is_default_mod(mod) and is_default_platform(platform):
        tags.append(pyver)
        if is_default_platform(platform):
            tags.append('latest')

    if mod == 'all':
        for t in list(tags):
            t = t.replace('all', 'all-jupyter')
            if t not in tags:
                tags.append(t)

    # for t in list(tags):
    #     if 'latest' not in t:
    #         tags.append('%s-ver%s' % (t, datetime.datetime.now().strftime('%y%m%d')))

    return tags


def get_job(tags):
    job_name = '_'.join(tags)[:99]
    build_scripts = indent(1, textwrap.dedent('''
        %s:
            runs-on: ubuntu-latest
            steps:
                - uses: actions/checkout@master
                - name: Free disk space
                  run: |
                    df -h
                    sudo apt-get autoremove -y
                    sudo apt-get clean
                    sudo swapoff -a
                    sudo rm -f /swapfile
                    docker rmi $(docker image ls -aq)
                    df -h
                - name: Build docker image
                  run: docker build %s -f docker/Dockerfile.%s .
                - name: Deploy docker image
                  run: |
                    docker login -u ${{secrets.DOCKER_USER}} -p ${{secrets.DOCKER_PASS}}
                    ''' % (
                    job_name,
                    ' '.join('-t ${{secrets.DOCKER_REPO}}:%s' % tag for tag in tags),
                    tags[0])))
    is_all = False
    is_cpu = False
    for tag in tags:
        build_scripts += indent(4, 'docker push ${{secrets.DOCKER_REPO}}:%s\n' % tag)
        if 'all' in tag:
            is_all = True
        if 'cpu' in tag:
            is_cpu = True
    if is_all and is_cpu:
        test_scripts = textwrap.dedent('''
            import tensorflow as m; print(m.__name__, ':', m.__version__);
            import mxnet as m; print(m.__name__, ':', m.__version__);
            from tensorflow import keras as m; print(m.__name__, ':', m.__version__);
            import torch as m; print(m.__name__, ':', m.__version__);
            import chainer as m; print(m.__name__, ':', m.__version__);
            import paddle as m; print(m.__name__, ':', m.__version__);
            ''').replace('\n', '')
        run_prefix = '- run: docker run ${{secrets.DOCKER_REPO}}:%s ' % tags[0]
        build_scripts += indent(3, textwrap.dedent('''
            %s python -c "%s"
            %s darknet
            ''' % (run_prefix, test_scripts, run_prefix)))

    build_scripts += '\n'
    return job_name, build_scripts


def write(f, scripts):
    for line in scripts.splitlines():
        f.write(line.rstrip())
        f.write('\n')


def generate(ci_fname):
    with open(ci_fname, 'w') as f:
        write(f, textwrap.dedent('''
            name: deepo CI
            on: [push]
            jobs:
        ''')[1:])

    job_names = []
    for fn in os.listdir(os.path.join('..', 'docker')):
        postfix = fn.split('.')[-1]
        tags = get_tags(postfix)
        job_name, build_scripts = get_job(tags)
        job_names.append(job_name)

        with open(ci_fname, 'a') as f:
            write(f, build_scripts)


if __name__ == '__main__':
    generate('../.github/workflows/dockerimage.yml')
