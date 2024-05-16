# Valmix

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/valmix/ci.yml?branch=main)](https://github.com/stephane-caron/valmix/actions)
[![Documentation](https://img.shields.io/github/actions/workflow/status/stephane-caron/valmix/docs.yml?branch=main&label=docs)](https://stephane-caron.github.io/valmix/)
[![Coverage](https://coveralls.io/repos/github/stephane-caron/valmix/badge.svg?branch=main)](https://coveralls.io/github/stephane-caron/valmix?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/valmix)](https://pypi.org/project/valmix/)

Adjust numerical values from a terminal user interface.

## Usage

Suppose you have a Python program with parameters you want to tune:

```py
def main(kp: float, kd: float):
    pass  # your code here
```

Valmix gives a systematic way to tune these parameters from the command line. First, wrap your parameters in ``multiprocessing.Value``s:

```py
import multiprocessing as mp

kp = mp.Value("f", 10.0)
kd = mp.Value("f", 1.0)
```

Next, update your program to read from the multiprocessing values. For example:

```py
import numpy as np
import time

def main(kp: mp.Value, kd: mp.Value):
    with open("/tmp/output", "w") as output:
        for _ in range(100):
            u = np.clip(kp.value * 1.0 + kd.value * 0.1, 5.0, 20.0)
            output.write(f"{u}\n")
            output.flush()
            time.sleep(1.0)

```

Finally, run your program and Valmix together, specifying the tuning range for each value:

```py
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
```

This will fire up a terminal user interface (TUI) where you can tune ``kp`` and ``kd`` while the program runs in the background:

![image](https://github.com/stephane-caron/valmix/assets/1189580/1d50ccf5-9bb2-4a73-95e3-9f3345a91311)

Useful for instance to [tune robot behaviors](https://github.com/upkie/upkie/blob/main/examples/wheeled_balancing.py) in real-time 😉

## Installation

### From PyPI

```console
pip install valmix
```

## See also

Related software:

- [Textual](https://textual.textualize.io/): terminal user interface (TUI) framework for Python, used to build this tool.
