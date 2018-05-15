# -*- coding: utf-8 -*-

"""Generate dockerfiles & CI configuration."""

import os
import textwrap


def indent(n, s):
    prefix = ' ' * 4 * n
    return ''.join(prefix + l for l in s.splitlines(True))


def get_tags(postfix, py_split='-py'):
    tags = [postfix]
    if postfix.endswith('-cu90'):
        tags.append(postfix[:-5])
    if py_split in postfix:
        name, platform = postfix.split(py_split)
        if platform == '36-cu90':
            tags.append(name)
        elif platform == '36-cpu':
            tags.append(name + '-cpu')
        if name == 'all':
            tags.append('py%s' % platform)
            if platform == '36-cu90':
                tags.append('latest')
            elif platform == '36-cpu':
                tags.append('cpu')
    return tags


def get_job(tags):
    job_name = '_'.join(tags)
    build_scripts = indent(1, textwrap.dedent('''
        "%s":
            machine: true
            steps:
                - checkout
                - run: docker build %s -f docker/Dockerfile.%s .
                - run: docker login -u $DOCKER_USER -p $DOCKER_PASS''' % (
                    job_name,
                    ' '.join('-t $DOCKER_REPO:%s' % tag for tag in tags),
                    tags[0])))
    for tag in tags:
        build_scripts += indent(3, textwrap.dedent('''
            - run: docker push $DOCKER_REPO:%s''' % tag))
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
