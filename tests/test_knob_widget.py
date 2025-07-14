#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0

"""Unit tests for the KnobWidget widget."""

import asyncio
import multiprocessing as mp
import unittest

import numpy as np

from valmix import Knob
from valmix.knob_widget import KnobWidget


class TestKnobWidget(unittest.TestCase):
    """Tests the KnobWidget widget."""

    def setUp(self):
        """Set up test fixtures."""
        # Create event loop if needed for Python 3.9 compatibility
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())

        self.value = mp.Value("i", 5)
        self.knob = Knob("test_knob", self.value, range(0, 10, 1))
        self.widget = KnobWidget(self.knob)

    def test_initialization(self):
        """Test widget initialization."""
        self.assertEqual(self.widget.knob, self.knob)
        self.assertEqual(self.widget.id, "test_knob-knob")

    def test_advance_updates_knob_and_ui(self):
        """Test that advance() updates both knob value and UI components."""
        initial_index = self.knob.current_index
        initial_value = self.knob.value

        # Mock UI components since we can't fully initialize them
        class MockProgressBar:
            def __init__(self):
                self.advanced_by = 0

            def advance(self, step):
                self.advanced_by += step

        class MockLabel:
            def __init__(self):
                self.updated_text = None

            def update(self, text):
                self.updated_text = text

        self.widget.progress_bar = MockProgressBar()
        self.widget.label = MockLabel()

        # Advance by a couple of steps
        self.widget.advance(2)

        # Check knob was advanced
        self.assertEqual(self.knob.current_index, initial_index + 2)
        self.assertEqual(self.knob.value, initial_value + 2)

        # Check UI was updated
        self.assertEqual(self.widget.progress_bar.advanced_by, 2)
        self.assertEqual(self.widget.label.updated_text, repr(self.knob))

    def test_advance_no_change_when_at_limit(self):
        """Test that advance() doesn't update the UI when knob is unchanged."""
        # Move to maximum position
        while self.knob.current_index < self.knob.nb_values - 1:
            self.knob.advance(1)

        class MockProgressBar:
            def __init__(self):
                self.advanced_by = 0

            def advance(self, step):
                self.advanced_by += step

        class MockLabel:
            def __init__(self):
                self.update_called = False

            def update(self, text):
                self.update_called = True

        self.widget.progress_bar = MockProgressBar()
        self.widget.label = MockLabel()

        # Try to advance beyond limit
        self.widget.advance(1)

        # UI should not be updated since knob didn't change
        self.assertEqual(self.widget.progress_bar.advanced_by, 0)
        self.assertFalse(self.widget.label.update_called)

    def test_float_knob_widget(self):
        """Test widget works with floating-point valued knobs."""
        float_value = mp.Value("f", 1.5)
        float_knob = Knob("float_test", float_value, np.arange(0.0, 5.0, 0.5))
        float_widget = KnobWidget(float_knob)

        self.assertEqual(float_widget.knob, float_knob)
        self.assertEqual(float_widget.id, "float_test-knob")
