import time
from multiprocessing import Process, Value


def add_one(p, a):
    for _ in range(3):
        print(f"in {p=}, {a.value=}")
        with a.get_lock():
            a.value += 1
        time.sleep(0.1)


if __name__ == "__main__":
    a = Value("i", 1)

    processes = []
    for _ in range(3):
        p = Process(target=add_one, args=(_, a))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
