#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Convenience function to run the app directly."""

from multiprocessing.sharedctypes import Synchronized as Value
from typing import Dict, Sequence, Tuple

from .app import App
from .knob import Knob, T


def run(tui: Dict[str, Tuple[Value, Sequence[T]]]) -> None:
    """Convenience function to run the app directly from the valmix module.

    Args:
        tui: Dictionary defining the terminal user interface.

    A TUI dictionary looks like this:

        {
            "foo": (mp.Value("f", 10.0), np.arange(0.0, 10.0, 0.5)),
            "bar": (mp.Value("i", 2), range(-7, 7)),
        }

    Each key defines a parameter whose value to tune. Each value (of the
    key-value dictionary) is a pair consisting of (1) a multiprocessing Value
    instance, holding the actual parameter to tune, and (2) the values the
    parameter may take, typically a range for integers or a NumPy linspace for
    floating-point numbers.
    """
    knobs = [Knob(key, value, values) for key, (value, values) in tui.items()]
    App(knobs).run()
