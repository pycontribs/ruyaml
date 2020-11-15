# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import datetime

# ToDo: you could probably attach the tzinfo correctly to the object
#       a more complete datetime might be used by safe loading as well

if False:  # MYPY
    from typing import Any, Dict, List, Optional  # NOQA


class TimeStamp(datetime.datetime):
    def __init__(self, *args, **kw):
        # type: (Any, Any) -> None
        self._yaml = dict(t=False, tz=None, delta=0)  # type: Dict[Any, Any]

    def __new__(cls, *args, **kw):  # datetime is immutable
        # type: (Any, Any) -> Any
        return datetime.datetime.__new__(cls, *args, **kw)  # type: ignore

    def __deepcopy__(self, memo):
        # type: (Any) -> Any
        ts = TimeStamp(
            self.year, self.month, self.day, self.hour, self.minute, self.second
        )
        ts._yaml = copy.deepcopy(self._yaml)
        return ts
