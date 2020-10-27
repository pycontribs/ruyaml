# coding: utf-8

import warnings

from ruyaml.util import configobj_walker as new_configobj_walker

if False:  # MYPY
    from typing import Any  # NOQA


def configobj_walker(cfg):
    # type: (Any) -> Any
    warnings.warn('configobj_walker has moved to ruyaml.util, please update your code')
    return new_configobj_walker(cfg)
