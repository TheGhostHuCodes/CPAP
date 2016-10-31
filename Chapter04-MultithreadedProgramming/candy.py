#!/usr/bin/env python3

from atexit import register
from random import randrange
from threading import BoundedSemaphore, Lock, Thread
from time import sleep, ctime

lock = Lock()
MAX = 5
candytray = BoundedSemaphore(MAX)


def refill():
    with lock:
        print("Refilling candy...", end="")
        try:
            candytray.release()
        except ValueError:
            print("Full, skipping")
        else:
            print("OK")


def buy():
    with lock:
        print("Buying candy...", end="")
        if candytray.acquire(False):
            print("OK")
        else:
            print("empty, skipping")


def producer(loops):
    for i in range(loops):
        refill()
        sleep(randrange(3))


def consumer(loops):
    for i in range(loops):
        buy()
        sleep(randrange(3))


def _main():
    print("starting at: {}".format(ctime()))
    nloops = randrange(2, 6)
    print("THE CANDY MACHINE (full with {} bars!)".format(MAX))
    Thread(
        target=consumer, args=(randrange(nloops, nloops + MAX + 2), )).start()
    Thread(target=producer, args=(nloops, )).start()


@register
def _atexit():
    print("ALL DONE at: {}".format(ctime()))


if __name__ == '__main__':
    _main()
