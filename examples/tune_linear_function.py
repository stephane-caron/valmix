#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Inria

"""Tune a linear function from the command line."""

import multiprocessing as mp
import time

import numpy as np

import valmix


def main(kp: mp.Value, kd: mp.Value):
    """A dummy program we want to tune.

    Args:
        kp: First tuning parameter.
        kd: Second tuning parameter.
    """
    with open("/tmp/output", "w") as output:
        for _ in range(15):
            u = np.clip(kp.value * 1.0 + kd.value * 0.1, 5.0, 20.0)
            output.write(f"{u}\n")
            output.flush()
            time.sleep(1.0)


if __name__ == "__main__":
    kp = mp.Value("f", 10.0)
    kd = mp.Value("f", 1.0)

    # Call the main function in a separate process
    main_process = mp.Process(target=main, args=(kp, kd))
    main_process.start()

    # Display the terminal user interface in this process (blocking call)
    valmix.run(
        {
            "kp": (kp, np.arange(0.0, 20.0, 0.5)),
            "kd": (kd, np.arange(0.0, 10.0, 0.5)),
        }
    )
