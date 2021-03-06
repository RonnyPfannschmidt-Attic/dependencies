from collections import Mapping
import weakref
from .utils import SimpleDelegate
import pytest
from _pytest.python import getfuncargnames


class ScopeDict(dict):
    def __init__(self, name):
        self.name = name
        self.cleanups = []

    def run_cleanups(self):
        while self.cleanups:
            cleanup = self.cleanups.pop()
            cleanup()

    def add_cleanup(self, cleanup):
        self.cleanups.append(cleanup)

    def __repr__(self):
        dr = dict.__repr__(self)
        return '<Scoped {name} {dr}>'.format(
                dr=dr,
                name=self.name,
                )


class Scopes(Mapping):
    def __init__(self, names):
        self.names = names
        self.stack = []

    @property
    def current(self):
        return self.stack[-1]

    def __getitem__(self, name):
        for item in reversed(self.stack):
            # use self as not found marker
            res = item.get(name, self)
            if res is not self:
                return res
        raise KeyError(name)

    def _key_set(self):
        keys = set()
        for item in self.stack:
            keys.update(item)
        return keys

    def __iter__(self):
        return iter(self._key_set())

    def add_cleanup(self, cleanup):
        self.current.add_cleanup(cleanup)

    def __len__(self):
        return len(self._key_set())

    def enter(self, name):
        assert self.names[len(self.stack)] == name
        self.stack.append(ScopeDict(name))

    def leave(self, name):
        assert self.stack[-1].name == name
        scope = self.stack.pop()
        scope.run_cleanups()

    def set(self, name, value):
        self.current[name] = value


class WrappedFunction(object):
    def __init__(self, callable, dm):
        self._callable = callable
        self._dm = dm

    def get_args(self):
        names = getfuncargnames(self._callable)
        result = {}
        for name in names:
            result[name] = self._dm.get(name)
        return result

    def call(self):
        args = self.get_args()
        return self._callable(**args)


class DependencyManager(object):
    def __init__(self, scopenames, wrap_call=WrappedFunction):
        self.scopes = Scopes(scopenames)
        self.wrap_call = wrap_call

    def enter_scope(self, name):
        self.scopes.enter(name)

    def get(self, name):
        return self.scopes.get(name)

    def call(self, function):
        function = self.wrap_call(function, self)
        return function.call()
