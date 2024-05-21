#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Unit tests for the Knob interface."""

import multiprocessing as mp
import unittest

import numpy as np

from valmix import Knob


class TestKnob(unittest.TestCase):
    """Tests the Knob interface."""

    def test_available_initial_value(self):
        v = mp.Value("i", 12)
        knob = Knob("v", v, range(5, 15, 1))
        self.assertEqual(knob.value, v.value)

    def test_out_of_range_initial_value(self):
        v = mp.Value("i", 12)
        knob = Knob("v", v, range(5, 15, 3))
        self.assertEqual(knob.value, 11)
        self.assertEqual(v.value, 11)

    def test_advance(self):
        v = mp.Value("f", 12.1)
        knob = Knob("v", v, np.arange(5, 15, 1.0))
        self.assertAlmostEqual(knob.value, 12.0)
        self.assertAlmostEqual(v.value, 12.0)
        knob.advance(+1)
        self.assertAlmostEqual(knob.value, 13.0)
        self.assertAlmostEqual(v.value, 13.0)
        knob.advance(-1)
        knob.advance(-1)
        self.assertAlmostEqual(knob.value, 11.0)
        self.assertAlmostEqual(v.value, 11.0)

    def test_advance_limits(self):
        v = mp.Value("i", 5)
        knob = Knob("v", v, range(5, 10, 3))
        self.assertEqual(knob.value, 5)
        for _ in range(3):
            knob.advance(+1)
            self.assertEqual(knob.value, 8)
        for _ in range(3):
            knob.advance(-1)
            self.assertEqual(knob.value, 5)
