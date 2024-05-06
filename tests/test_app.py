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

    async def test_run(self):
        foo = valmix.Knob("foo", mp.Value("i"), range(-10, 10, 3))
        bar = valmix.Knob("baz", mp.Value("f"), np.arange(-1.0, 3.0, 0.1))
        app = valmix.App([foo, bar])
        async with app.run_test() as pilot:
            await pilot.click("#foo")
            self.assertEqual(app.focused.id, "foo")
            await pilot.click("#baz")
            self.assertEqual(app.focused.id, "baz")
