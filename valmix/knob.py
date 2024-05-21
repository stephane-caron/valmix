#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Knob interface."""

from multiprocessing.sharedctypes import Synchronized as Value
from typing import Sequence, Union

T = Union[int, float]


class Knob:
    """Name and list values for a target quantity."""

    def __init__(
        self,
        name: str,
        value: Value,
        values: Sequence[T],
    ) -> None:
        """Create a new knob.

        Args:
            name: Display name of the value.
            value: Actual multiprocessing synchronized shared object.
            values: Values the internal value may take.
        """
        nb_values = len(values)
        initial_value = value.value
        self.__index = nb_values // 2
        self.__mp_value = value
        self.__name = name
        self.__nb_values = nb_values
        self.__values = sorted(values)
        #
        self.__snap_to(initial_value)
        self.__update_mp_value()

    def __snap_to(self, snap_value: T) -> None:
        """Snap to available value closest to a given one.

        Args:
            snap_value: Quantity to get close to using values from the set.
        """
        self.__index = 0
        best_dist = abs(self.__values[0] - snap_value)
        for i in range(1, self.__nb_values):
            cur_dist = abs(self.__values[i] - snap_value)
            if cur_dist < best_dist:
                self.__index = i
                best_dist = cur_dist

    def __update_mp_value(self) -> None:
        """Update internal multiprocessing value from current index."""
        new_value = self.__values[self.__index]
        with self.__mp_value.get_lock():
            self.__mp_value.value = new_value

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
        self.__update_mp_value()

    @property
    def current_index(self) -> int:
        """Get current index in the list of available values.

        Returns:
            Current index of the knob.
        """
        return self.__index

    @property
    def value(self) -> T:
        """Get current value of the knob.

        Returns:
            Current value of the knob.
        """
        return self.__mp_value.value

    @property
    def name(self) -> str:
        """Knob name to display."""
        return self.__name

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
        v = self.value
        if isinstance(v, float):
            return f"{v:.2f}" if 1e-2 <= abs(v) < 100.0 else f"{v:.1e}"
        return str(self.value)
