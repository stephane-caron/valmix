#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""KnobWidget widget definition."""

from textual.app import ComposeResult
from textual.containers import Widget
from textual.widgets import Button, Label, ProgressBar

from .knob import Knob


class KnobWidget(Widget):
    """Widget combining a focus button, a progress bar and a value label.

    Attributes:
        knob: Knob associated with the widget.
    """

    DEFAULT_CSS = r"""

    KnobWidget {
        height: 3;
        layout: horizontal;
    }

    KnobWidget Button,
    KnobWidget Button:enabled, {
        border: wide $primary;
        margin: 0 2;
        width: 3;
    }

    KnobWidget Button:focus {
        background: $accent;
    }

    KnobWidget ProgressBar {
        margin: 1 3;
        width: 6fr;
    }

    KnobWidget Bar {
        width: 1fr;
    }

    KnobWidget PercentageStatus {
        display: none;
    }

    KnobWidget Label {
        margin: 1 2;
        width: 8;
    }

    """

    knob: Knob
    label: Label
    progress_bar: ProgressBar

    def __init__(self, knob: Knob):
        """Create a new widget.

        Args:
            knob: Knob associated with the widget.
        """
        self.knob = knob
        self.label = Label()  # updated by compose()
        self.progress_bar = ProgressBar()  # updated by compose()
        super().__init__(id=f"{knob.name}-knob")

    def compose(self) -> ComposeResult:
        """Render the widget."""
        yield Button(self.knob.name, id=self.knob.name)

        self.progress_bar = ProgressBar(
            total=self.knob.nb_values - 1,
            show_eta=False,
            show_percentage=True,
            id=f"{self.knob.name}-bar",
        )
        self.progress_bar.advance(self.knob.current_index)
        yield self.progress_bar

        self.label = Label(repr(self.knob), id=f"{self.knob.name}-value")
        yield self.label

    def advance(self, step: int):
        """Advance the underlying knob by a number of steps.

        Args:
            step: Number of steps to add to advance the knob by.
        """
        previous_index = self.knob.current_index
        self.knob.advance(step)
        if self.knob.current_index == previous_index:
            return
        self.progress_bar.advance(step)  # can advance beyond its total
        self.label.update(repr(self.knob))
