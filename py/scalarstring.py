from __future__ import absolute_import
from __future__ import print_function

__all__ = ["ScalarString", "PreservedScalarString"]

from .compat import text_type


class ScalarString(text_type):
    def __new__(cls, *args, **kw):
        return text_type.__new__(cls, *args, **kw)


class PreservedScalarString(ScalarString):
    def __new__(cls, value):
        return ScalarString.__new__(cls, value)
