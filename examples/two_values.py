#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Adjust two numerical values from a terminal user interface.

The value "foo" is an integer in a custom range, while the value "bar" is a
floating point number living in a custom NumPy array range.
"""

import multiprocessing as mp

import numpy as np

import valmix

if __name__ == "__main__":
    foo = valmix.Knob("foo", mp.Value("i"), range(-10, 10, 3))
    bar = valmix.Knob("bar", mp.Value("f"), np.arange(-1.0, 3.0, 0.1))
    app = valmix.App([foo, bar])
    app.run()