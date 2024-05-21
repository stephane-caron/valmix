#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Unit tests for the run function."""

import multiprocessing as mp
import unittest

import numpy as np

import valmix


class TestRun(unittest.TestCase):
    """Tests for the main valmix.run function."""

    def test_run(self):
        # RuntimeError: There is no current event loop in thread 'MainThread'.
        with self.assertRaises(RuntimeError):
            valmix.run(
                {
                    "foo": (mp.Value("i", 0), range(-10, 10, 3)),
                    "baz": (mp.Value("f", 1.0), np.arange(-1.0, 3.0, 0.1)),
                },
            )
