#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Main application screen."""

from typing import List

import textual.app
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header

from .knob import Knob
from .knob_widget import KnobWidget


class App(textual.app.App):
    """Valmix application.

    Attributes:
        knobs: Knobs manipulated via the app interface.
    """

    TITLE = "Valmix"

    BINDINGS = [
        Binding(key="down,j", action="next", description="Next"),
        Binding(key="up,k", action="previous", description="Previous"),
        Binding(key="left,h", action="decrease", description="Decrease"),
        Binding(key="right,l", action="increase", description="Increase"),
        Binding(key="q", action="quit", description="Quit"),
    ]

    def __init__(self, knobs: List[Knob]) -> None:
        """Initialize application.

        Args:
            knobs: Knobs manipulated via the app interface.
        """
        self.knobs = {knob.name: knob for knob in knobs}
        super().__init__()

    def compose(self) -> ComposeResult:
        """Compose the application screen."""
        yield Header()
        for knob in self.knobs.values():
            yield KnobWidget(knob)
        yield Footer()

    def action_decrease(self) -> None:
        """Decrease currently-selected knob."""
        if self.focused is not None:
            knob = self.query_one(f"#{self.focused.id}-knob")
            if isinstance(knob, KnobWidget):  # should be the case
                knob.advance(-1)

    def action_increase(self) -> None:
        """Increase currently-selected knob."""
        if self.focused is not None:
            knob = self.query_one(f"#{self.focused.id}-knob")
            if isinstance(knob, KnobWidget):  # should be the case
                knob.advance(+1)

    def action_previous(self) -> None:
        """Focus previous knob."""
        self.screen.focus_previous()

    def action_next(self) -> None:
        """Focus next knob."""
        self.screen.focus_next()
