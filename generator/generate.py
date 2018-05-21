# -*- coding: utf-8 -*-

"""Console script for generator."""
import argparse
from core.composer import Composer


def _import(name):
    mname = name.lower()
    cname = name.title()
    mod = __import__('modules.%s' % mname, fromlist=[cname])
    mod = getattr(mod, cname)
    return mod


def main():
    """
    Generate a dockerfile according to the given modules to be installed.
    """
    parser = argparse.ArgumentParser(description='Composer')
    parser.add_argument('path')
    parser.add_argument('modules', nargs='*')
    parser.add_argument('--cuda-ver')
    parser.add_argument('--cudnn-ver')
    args = parser.parse_args()

    in_modules = []
    versions = {}
    for module in args.modules:
        terms = module.split('==')
        m = _import(terms[0])
        in_modules.append(m)
        if len(terms) > 1:
            versions[m] = terms[1]
    composer = Composer(in_modules, args.cuda_ver, args.cudnn_ver, versions)
    with open(args.path, 'w') as f:
        f.write(composer.to_dockerfile())


if __name__ == "__main__":
    main()
