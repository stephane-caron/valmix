#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Unit tests for the Knob interface."""

import unittest
import multiprocessing as mp

from valmix import Knob


class TestKnow(unittest.TestCase):
    """Tests the Knob interface."""

    def test_available_initial_value(self):
        v = mp.Value("i", 12)
        knob = Knob("v", v, range(5, 15, 1))
        self.assertEqual(knob.current_value, v.value)

    def test_out_of_range_initial_value(self):
        v = mp.Value("i", 12)
        knob = Knob("v", v, range(5, 15, 3))
        self.assertEqual(knob.current_value, 11)
        self.assertEqual(v.value, 11)
