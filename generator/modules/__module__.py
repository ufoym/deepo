# -*- coding: utf-8 -*-


def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


@parametrized
def dependency(module, *_deps):
    module.deps = _deps
    return module


@parametrized
def source(module, _source):
    module.source = _source
    return module


@parametrized
def version(module, _ver):
    module.version = _ver
    return module


@dependency()
@source('unknown')
@version('latest')
class Module(object):

    def __init__(self, composer):
        self.composer = composer

    def __repr__(self):
        return '%-13s %-6s (%s)' % (
            self.name(),
            self.version,
            self.source)

    def build(self):
        pass

    def expose(self):
        return []

    def name(self):
        return self.__class__.__name__.lower()
