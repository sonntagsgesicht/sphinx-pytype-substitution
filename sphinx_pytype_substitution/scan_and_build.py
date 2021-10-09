# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.10, copyright Monday, 04 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)

from inspect import isclass, ismodule, getmodule, ismethod, getmembers
from os import linesep
from re import match

ROLES = {'mod': ':py:mod:',
         'cls': ':py:class:',
         'obj': ':py:obj:',
         'func': ':py:func:',
         'meth': ':py:meth:',
         'attr': ':py:attr:',
         'exc': ':py:exc:',
         'const': ':py:const:'}


# add substitutions as
# subs.type[mod.cls.attr()] = <mod.cls.attr>
# to add the following to rst_epilog
# .. type:`mod.cls.attr() <mod.cls.attr>`


class SubstitutionCollection(object):

    @property
    def names(self):
        return tuple(sorted(self.keys()))

    @property
    def roles(self):
        return tuple(self.role(n) for n in self.names)

    def __init__(self, **kwargs):
        self.mod = kwargs.get('mod', dict())
        self.cls = kwargs.get('cls', dict())
        self.obj = kwargs.get('obj', dict())
        self.func = kwargs.get('func', dict())
        self.meth = kwargs.get('meth', dict())
        self.attr = kwargs.get('attr', dict())
        self.exc = kwargs.get('exc', dict())
        self.const = kwargs.get('const', dict())

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        return setattr(self, item, value)

    def keys(self):
        return (a for a, v in self.__dict__.items()
                if not a.startswith('_') and not callable(v))

    def values(self):
        return (getattr(self, name) for name in self.keys())

    def items(self):
        return ((name, getattr(self, name)) for name in self.keys())

    def get(self, item, default=None):
        return self[item] if item in self.keys() else default

    def update(self, other):
        for name, value in self.items():
            self[name].update(other.get(name, dict()))

    def filter(self, function_or_none=None):
        for name in self.keys():
            # self[name] = dict(filter(function_or_none, self[name].items()))
            self[name] = dict((k, v) for k, v in self[name].items()
                              if function_or_none(k, v))
        return self

    def exclude(self, pattern):
        return self.filter(lambda v: match(pattern, v) is None) \
            if pattern else self

    def match(self, pattern):
        return self.filter(lambda k, v: match(pattern, v) is not None) \
            if pattern else self

    def shorten_keys(self):
        short = dict()
        for name in self.names:
            dic = dict()
            for (*keys,), value in getattr(self, name).items():
                if keys[-1] in dic:
                    return SubstitutionCollection()
                dic[(keys[-1],)] = value
            short[name] = dic
        return SubstitutionCollection(**short)

    @staticmethod
    def _issub(sub, mod):
        return sub and mod and sub.__name__.startswith(mod.__name__)

    def extract_module(self, mod):
        # as module  'datetime': '<datetime>'
        # as class 'time': <time>' + members ..
        # as func  'foo()': 'datetime.foo() <datetime.foo>'
        # as attr  'date.year ': '<datetime.date.year>'
        if not ismodule(mod):
            return self
        self.mod[(mod.__name__,)] = mod.__name__

        for name, attr in getmembers(mod):
            # ignore
            if name.startswith('_'):
                continue
            if getmodule(attr) and \
                    not self._issub(getmodule(attr), mod):
                continue

            # add
            if ismodule(attr):
                self.extract_module(attr)
            elif isclass(attr):
                self.extract_class(attr)
            elif callable(attr):
                self.func[
                    (mod.__name__, name + '()')] = mod.__name__ + '.' + name
            else:
                if name == name.upper():
                    self.const[
                        (mod.__name__, name)] = mod.__name__ + '.' + name
                else:
                    self.attr[(mod.__name__, name)] = mod.__name__ + '.' + name
        return self

    def extract_class(self, cls):
        # as exec  'ValueError': '<ValueError>'
        # as class  'date': '<datetime.date>'
        # as instance  'date()': '<datetime.date>'
        # as class methode  'date.today()', '<datetime.date.today>'
        # as static methode  'date().today()', '<datetime.date.today>'
        # as instance methode 'date().today()': '<datetime.date.today>'
        # as class attr  'date.year': '<datetime.date.year>'
        # as instance attr  'date().year': '<datetime.date.year>'
        if not isclass(cls):
            return self

        m_c_name = cls.__module__ + '.' + cls.__qualname__
        if issubclass(cls, Exception):
            self.exc[(cls.__module__, cls.__qualname__)] = m_c_name
            return self

        self.cls[(cls.__module__, cls.__qualname__)] = m_c_name
        self.cls[(cls.__module__, cls.__qualname__ + '()')] = m_c_name

        for name, attr in getmembers(cls):
            # ignore
            if name.startswith('_'):
                continue
            if getmodule(attr) and \
                    not self._issub(getmodule(attr), getmodule(cls)):
                continue

            # add
            m_c_a_name = cls.__module__ + '.' + cls.__qualname__ + '.' + name
            if ismodule(attr):
                self.extract_module(attr)
            elif isclass(attr):
                self.extract_class(attr)
            elif callable(attr):
                if ismethod(attr):
                    self.meth[
                        (cls.__module__,
                         cls.__qualname__ + '.' + name + '()')] = m_c_a_name
                else:
                    self.func[
                        (cls.__module__,
                         cls.__qualname__ + '().' + name + '()')] = m_c_a_name
            else:
                if name == name.upper():
                    self.const[
                        (cls.__module__,
                         cls.__qualname__ + '.' + name)] = m_c_a_name
                else:
                    self.attr[
                        (cls.__module__,
                         cls.__qualname__ + '().' + name)] = m_c_a_name
        return self

    def substitutions(self, names=()):
        names = names if names else self.names
        lines = list()
        for name in names:
            for key, value in self[name].items():
                ref = key if value is None else value
                line = ".. |%s|" % '.'.join(key)
                line = line.ljust(50)
                line += "replace:: :%s:`<%s>`" % (self.role(name), ref)
                lines.append(line)
        return lines

    @staticmethod
    def role(name):
        role_name = 'class' if name == 'cls' else name
        return ':py:%s:' % str(role_name)

    def __str__(self):
        return """   %s""" % (linesep + "   ").join(self.substitutions())

    def __len__(self):
        return sum(len(v) for v in self.values())


def rst_epilog(*objs, match_pattern='', exclude_pattern='', short=False):
    coll = SubstitutionCollection()
    for obj in objs:
        if ismodule(obj):
            coll.extract_module(obj)
        elif isclass(obj):
            coll.extract_class(obj)
        else:
            raise TypeError(
                "object of type %s can't be handled." % type(obj))
    coll.match(match_pattern)
    coll.exclude(exclude_pattern)
    if short:
        coll = coll.shorten_keys()
    return str(coll)


if __name__ == '__main__':
    import datetime, os, sys, businessdate, dcf

    print(tuple(SubstitutionCollection().names))
    # s = SubstitutionCollection().extract_module(dcf).shorten_keys()
    # print(len(s))
    print(rst_epilog(businessdate, match_pattern='', short=True))
