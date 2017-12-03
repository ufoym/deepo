# -*- coding: utf-8 -*-

"""Console script for generator."""
import click
from core.composer import Composer


def _import(name):
    mname = name.lower()
    cname = name.title()
    mod = __import__('modules.%s' % mname, fromlist=[cname])
    mod = getattr(mod, cname)
    return mod


@click.command()
@click.argument('path', nargs=1)
@click.argument('modules', nargs=-1)
@click.option('--cpu-only', is_flag=True)
def main(path, modules, cpu_only):
    """
    Generate a dockerfile according to the given modules to be installed.
    """
    in_modules = []
    versions = {}
    for module in modules:
        terms = module.split('==')
        m = _import(terms[0])
        in_modules.append(m)
        if len(terms) > 1:
            versions[m] = terms[1]
    composer = Composer(in_modules, versions, cpu_only=cpu_only)
    with open(path, 'w') as f:
        f.write(composer.to_dockerfile())


if __name__ == "__main__":
    main()
