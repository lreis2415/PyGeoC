#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests of MathClass in pygeoc.utils

    @author: Liangjun Zhu

    @changlog:
    - 17-09-16 lj - origin version.
"""
from pygeoc.utils import MathClass
import pytest


def test_mathclass_isnumerical():
    assert MathClass.isnumerical('78') == True
    assert MathClass.isnumerical('1.e-5') == True
    assert MathClass.isnumerical(None) == False
    assert MathClass.isnumerical('a1.2') == False