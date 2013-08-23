from collections import Mapping



class SimpleDelegate(object):
    def __init__(self, attribute, method):
        self.attribute = attribute
        self.method = method

    def __get__(self, instance, type):
        if instance is not None:
            obj = getattr(instance, self.attribute)
            return getattr(obj, self.method)
        return self

    def __set__(self, instance, type):
        if instance is None:
            super(SimpleDelegate, self).__set__(instance, type)

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

class DependencyManager(object):
    def __init__(self, scopenames):
        self.scopes = Scopes(scopenames)

    enter_scope = SimpleDelegate('scopes', 'enter')
    leave_scope = SimpleDelegate('scopes', 'leave')
    set = SimpleDelegate('scopes', 'set')
