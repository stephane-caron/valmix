#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

import multiprocessing as mp
from typing import Sequence


class Knob:
    r"""Name and list values for a target quantity.

    Attributes:
        name: Display name of the value.
        value: Actual multiprocessing synchronized shared object.
        choices: Values the internal value may take.
    """

    name: str
    value: mp.Value
    choices: Sequence

    def __init__(self, name: str, value: mp.Value, choices: Sequence):
        self.name = name
        self.value = value
        self.choices = sorted(choices)
