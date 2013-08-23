
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
