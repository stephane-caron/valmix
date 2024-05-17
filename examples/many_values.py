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
    valmix.run(
        {
            # Syntax:
            # "name": (mp.Value("<type>", <initial_value>), <possible_values>)
            "foo": (mp.Value("i", 0), range(-10, 10, 3)),
            "bar": (mp.Value("f", 1.0), np.arange(-1.0, 3.0, 0.1)),
            "kp": (mp.Value("f", 1.0), np.arange(0.1, 10.0, 0.1)),
            "kd": (mp.Value("f", 0.0), np.arange(0.0, 10.0, 0.1)),
            "alpha": (mp.Value("f", 1.0), np.arange(-10.0, 10.0, 0.5)),
            "beta": (mp.Value("i", 0), range(20)),
        }
    )
