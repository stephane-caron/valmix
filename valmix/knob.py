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
        values: Values the internal value may take.
    """

    name: str
    value: mp.Value
    values: Sequence

    def __init__(self, name: str, value: mp.Value, values: Sequence):
        nb_values = len(values)
        self.name = name
        self.value = value
        self.values = sorted(values)
        self.__index = nb_values // 2
        self.__nb_values = nb_values

    def advance(self, step: int):
        self.__index += step
        if self.__index >= self.__nb_values:
            self.__index = self.__nb_values - 1
        elif self.__index < 0:
            self.__index = 0

    @property
    def current_index(self):
        return self.__index

    @property
    def current_value(self):
        return self.values[self.__index]

    @property
    def nb_values(self) -> int:
        return self.__nb_values

    def __repr__(self) -> str:
        v = self.current_value
        if isinstance(v, float):
            return f"{v:.2}" if 1e-2 <= v < 100.0 else f"{v:.1e}"
        return str(self.current_value)
