#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Knob interface."""

import multiprocessing as mp
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


class Knob(Generic[T]):
    r"""Name and list values for a target quantity.

    Attributes:
        name: Display name of the value.
        value: Actual multiprocessing synchronized shared object.
        values: Values the internal value may take.
    """

    name: str
    value: mp.Value
    values: Sequence

    def __init__(
        self,
        name: str,
        value: mp.Value,
        values: Sequence[T],
    ) -> None:
        """Create a new knob.

        Args:
            name: Display name of the value.
            value: Actual multiprocessing synchronized shared object.
            values: Values the internal value may take.
        """
        nb_values = len(values)
        self.name = name
        self.value = value
        self.values = sorted(values)
        self.__index = nb_values // 2
        self.__nb_values = nb_values
        #
        self.__snap_to(value.value)
        self.__update_value()

    def advance(self, step: int) -> None:
        """Advance to the next value listed when configuring the knob.

        Args:
            step: Number of steps to add to the list index.
        """
        self.__index += step
        if self.__index >= self.__nb_values:
            self.__index = self.__nb_values - 1
        elif self.__index < 0:
            self.__index = 0
        self.__update_value()

    def __snap_to(self, snap_value: T) -> None:
        self.__index = 0
        cur_value = self.values[0]
        for i in range(self.__nb_values):
            if abs(self.values[i] - snap_value) < abs(cur_value - snap_value):
                self.__index = i
                cur_value = self.values[i]

    def __update_value(self) -> None:
        new_value = self.values[self.__index]
        with self.value.get_lock():
            self.value.value = new_value

    @property
    def current_index(self) -> int:
        """Get current index in the list of available values.

        Returns:
            Current index of the knob.
        """
        return self.__index

    @property
    def current_value(self) -> T:
        """Get current value of the knob.

        Returns:
            Current value of the knob.
        """
        return self.value.value

    @property
    def nb_values(self) -> int:
        """Get the number of different values that the knob can take.

        Returns:
            Number of different values that the knob can take.
        """
        return self.__nb_values

    def __repr__(self) -> str:
        """Get a string representation of the knob's value.

        Returns:
            String representation of the current value of the knob.
        """
        v = self.current_value
        if isinstance(v, float):
            return f"{v:.2}" if 1e-2 <= abs(v) < 100.0 else f"{v:.1e}"
        return str(self.current_value)
