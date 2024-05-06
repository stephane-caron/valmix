#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

from textual.app import ComposeResult
from textual.containers import Widget
from textual.widgets import Button, Label, ProgressBar

from .knob import Knob


class Mixer(Widget):

    DEFAULT_CSS = r"""

    Mixer {
        height: 3;
        layout: horizontal;
    }

    Mixer Button,
    Mixer Button:enabled, {
        border: wide green;
        margin: 0 2;
        width: 3;
    }

    Mixer Button:focus {
        background: $accent;
    }

    Mixer ProgressBar {
        margin: 1 3;
        width: 6fr;
    }

    Mixer Bar {
        width: 1fr;
    }

    Mixer PercentageStatus {
        display: none;
    }

    Mixer Label {
        margin: 1 2;
        width: 8;
    }

    """

    def __init__(self, knob: Knob):
        self.knob = knob
        super().__init__(id=f"{knob.name}-mixer")

    def compose(self) -> ComposeResult:
        self.button = Button(self.knob.name, id=self.knob.name)
        yield self.button

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
        previous_index = self.knob.current_index
        self.knob.advance(step)
        if self.knob.current_index == previous_index:
            return
        self.progress_bar.advance(step)  # can advance beyond its total
        self.label.update(repr(self.knob))
