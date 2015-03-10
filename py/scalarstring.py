from __future__ import absolute_import
from __future__ import print_function

__all__ = ["ScalarString"]


class ScalarString(str):
    pass


class PreservedScalarString(ScalarString):
    def __init__(self, value):
        ScalarString.__init__(self, value)