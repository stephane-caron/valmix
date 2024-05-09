#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Convenience function to run the app directly."""

from typing import List

from .app import App
from .knob import Knob


def run(knobs: List[Knob]) -> None:
    """Convenience function to run the app directly from the valmix module.

    Args:
        knobs: Knobs manipulated via the app interface.
    """
    App(knobs).run()
