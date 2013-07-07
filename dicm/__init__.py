from collections import Mapping



class SimpleDelegate(object):
    def __init__(self, attribute, method):
        self.attribute = attribute
        self.method = method

    def __get__(self, instance, type):
        if instance is not None:
            obj = getattr(instance, self.attribute)
            return getattr(obj, self.method)

class ScopeDict(dict):
    def __init__(self, name):
        self.name = name
        self.cleanups = []

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

    def __len__(self):
        return len(self._key_set())

    def enter(self, name):
        assert name in self.names
        self.stack.append(ScopeDict(name))

    def leave(self, name):
        assert self.stack[-1].name == name
        self.stack.pop()

class DependencyManager(object):
    def __init__(self, scopenames):
        self.scopes = Scopes(scopenames)

    enter_scope = SimpleDelegate('scopes', 'enter')
    leave_scope = SimpleDelegate('scopes', 'leave')
