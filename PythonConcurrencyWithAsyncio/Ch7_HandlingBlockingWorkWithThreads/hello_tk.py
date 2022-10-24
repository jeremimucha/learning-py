#!/usr/bin/env python3
from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import tkinter
from tkinter import ttk


def say_hello():
    print('Hello there!')


def main():
    window = tkinter.Tk()
    window.title('Hello world app')
    window.geometry('200x100')

    hello_button = ttk.Button(window, text='Say Hello', command=say_hello)
    hello_button.pack()

    window.mainloop()


if __name__ == '__main__':
    main()
