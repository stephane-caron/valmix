#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Unit tests for the overall app."""

import multiprocessing as mp
import unittest

import numpy as np

import valmix


class TestApp(unittest.IsolatedAsyncioTestCase):
    """Tests for valmix.App."""

    def setUp(self):
        foo = valmix.Knob("foo", mp.Value("i", 0), range(-10, 10, 3))
        bar = valmix.Knob("baz", mp.Value("f"), np.arange(-1.0, 3.0, 0.1))
        self.app = valmix.App([foo, bar])

    async def test_click(self):
        async with self.app.run_test() as pilot:
            await pilot.click("#foo")
            self.assertEqual(self.app.focused.id, "foo")
            await pilot.click("#baz")
            self.assertEqual(self.app.focused.id, "baz")

    async def test_decrease(self):
        async with self.app.run_test() as pilot:
            await pilot.click("#foo")
            self.assertEqual(self.app.focused.id, "foo")
            knob = self.app.query_one(f"#{self.app.focused.id}-knob").knob
            self.assertEqual(knob.value, -1)
            await pilot.press("h")
            self.assertEqual(knob.value, -4)
