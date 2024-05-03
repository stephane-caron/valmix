import multiprocessing as mp

import numpy as np

import valmix

if __name__ == "__main__":
    foo = valmix.Knob("foo", mp.Value("i"), range(-10, 10, 3))
    bar = valmix.Knob("bar", mp.Value("f"), np.arange(-1.0, 3.0, 0.1))
    app = valmix.App([foo, bar])
    app.run()
