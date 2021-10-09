
from inspect import isbuiltin, isfunction, getmembers as _get_members, \
    ismodule, isclass, getmodule


def getmembers(obj, mod):
    obj_mod = getattr(obj, '__module__', '')
    for name, mem in _get_members(obj):
        if name.startswith('_'):
            continue
        if issubmodule(getmodule(mem), mod):
            yield name, mem
        if ismodule(mem):
            continue
        elif isclass(mem):
            continue
        elif iscallable(mem) and ismodule(obj):
            continue
        else:
            yield name, mem


def issubmodule(sub, mod):
    return sub and mod and sub.startswith(mod)


def iscallable(obj):
    return callable(obj)


def ismember(obj):
    bound_to = getattr(obj, '__self__', None)
    return isinstance(bound_to, type)


def isclassmember(attr):
    # must be bound to a class with attr as attribute
    return hasattr(getattr(attr, '__self__', None), attr.__name__)


def isclassmethod(cls, attr):
    if hasattr(attr, '__self__'):
        print(cls.__name__==attr.__self__.__name__, attr.__name__, attr.__self__.__mro__)
    else:
        print(attr)
