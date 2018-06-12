#python3

import tkinter
from tkinter import ttk


class MainWindow(ttk.Frame):
    """docstring for MainWindow"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row=0, column=0)
        self.principal = tkinter.DoubleVar()
        self.principal.set(1000.0)
        self.rate = tkinter.DoubleVar()
        self.rate.set(5.0)
        self.years = tkinter.IntVar()
        self.amount = tkinter.StringVar()
        principalLabel = ttk.Label(self, text="Principal $:",
            anchor=tkinter.W, underline=0)
        principalScale = tkinter.Scale(self, variable=self.principal,
            command=self.updateUi, from_=100, to=1000000,
            resolution=100, orient=tkinter.HORIZONTAL)
        rateLabel = ttk.Label(self, text="Rate %:", underline=0,
            anchor=tkinter.W)
        rateScale = tkinter.Scale(self, variable=self.rate,
            command=self.updateUi, from_=1, to=100, resolution=0.25,
            digits=5, orient=tkinter.HORIZONTAL)
        yearsLabel = tkinter.Label(self, text="Years:", underline=0,
            anchor=tkinter.W)
        yearsScale = tkinter.Scale(self, variable=self.years,
            command=self.updateUi, from_=1, to=50, orient=tkinter.HORIZONTAL)
        amountLabel = ttk.Label(self, text="Amount $", anchor=tkinter.W)
        actualAmountLabel = ttk.Label(self, textvariable=self.amount,
            relief=tkinter.SUNKEN, anchor=tkinter.E)

        principalLabel.grid(row=0, column=0, padx=2, pady=2,
            sticky=tkinter.W)
        principalScale.grid(row=0, column=1, padx=2, pady=2,
            sticky=tkinter.EW)
        rateLabel.grid(row=1, column=0, padx=2, pady=2, sticky=tkinter.W)
        rateScale.grid(row=1, column=1, padx=2, pady=2, sticky=tkinter.EW)
        yearsLabel.grid(row=2, column=0, padx=2, pady=2, sticky=tkinter.W)
        yearsScale.grid(row=2, column=1, padx=2, pady=2, sticky=tkinter.EW)
        amountLabel.grid(row=3, column=0, padx=2, pady=2, sticky=tkinter.W)
        actualAmountLabel.grid(row=3, column=1, padx=2, pady=2,
            sticky=tkinter.EW)

        principalScale.focus_set()
        self.updateUi()
        parent.bind("<Alt-p>", lambda *ignore: principalScale.focus_set())
        parent.bind("<Alt-r>", lambda *ignore: rateScale.focus_set())
        parent.bind("<Alt-y>", lambda *ignore: yearsScale.focus_set())
        parent.bind("<Control-q>", self.quit)
        parent.bind("<Escape>", self.quit)

    def updateUi(self, *ignore):
        amount = self.principal.get() * (
            (1 + (self.rate.get() / 100.0)) ** self.years.get())
        self.amount.set("{0:.2f}".format(amount))

    def quit(self, event=None):
        self.parent.destroy()


application = tkinter.Tk()
# path = os.path.join(os.path.dirname(__file__), "images/")
# if sys.platform.startswith("win"):
#     icon = path + "interest.ico"
# else:
#     icon = "@" + path + "interest.xbm"
# application.iconbitmap(icon)
application.title("Interest")
window = MainWindow(application)
application.protocol("WM_DELETE_WINDOW", window.quit)
application.mainloop()
