#! python3
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
try:
    Spinbox = ttk.Spinbox
except AttributeError:
    Spinbox = tk.Spinbox


APPNAME = "Hex View"
BLOCK_WIDTH = 16
BLOCK_HEIGHT = 32
BLOCK_SIZE = BLOCK_WIDTH * BLOCK_HEIGHT
ENCODINGS = ("ASCII", "CP037", "CP1140", "CP1252", "Latin1", "ISO8859_15",
             "Mac_Roman", "UTF-8", "UTF-8-sig", "UTF-16", "UTF-32")


class MainWindow:

    def __init__(self, parent):
        self.parent = parent
        self.create_variables()
        self.create_widgets()
        self.create_layout()
        self.create_bindings()
        if len(sys.argv) > 1:
            self._open(sys.argv[1])

    def create_variables(self):
        self.filename = None
        self.offset = tk.IntVar()
        self.offset.set(0)
        self.encoding = tk.StringVar()
        self.encoding.set(ENCODINGS[0])

    def create_widgets(self):
        frame = self.frame = ttk.Frame(self.parent)
        self.openButton = ttk.Button(frame, text='Open...', underline=0,
                                    command=self.open)
        self.offsetLabel = ttk.Label(frame, text="Offset", underline=1)
        self.offsetSpinbox = Spinbox(
            frame, from_=0, textvariable=self.offset, increment=BLOCK_SIZE)
        self.encodingLabel = ttk.Label(frame, text="Encoding", underline=0)
        self.encodingCombobox = ttk.Combobox(
            frame, values=ENCODINGS, textvariable=self.encoding,
            state="readonly")
        self.quitButton = ttk.Button(frame, text="Quit", underline=0,
                                    command=self.quit)
        self.create_view()

    def create_view(self):
        self.viewText = tk.Text(self.frame, height=BLOCK_HEIGHT,
                                width=2 + (BLOCK_WIDTH * 4))
        self.viewText.tag_configure('ascii', foreground='green')
        self.viewText.tag_configure('error', foreground='red')
        self.viewText.tag_configure('hexspace', foreground='navy')
        self.viewText.tag_configure('graybg', background='lightgray')

    def create_layout(self):
        for column, widget in enumerate((
                self.openButton, self.offsetLabel, self.offsetSpinbox,
                self.encodingLabel, self.encodingCombobox,
                self.quitButton)):
            widget.grid(row=0, column=column, sticky=tk.W)
        self.viewText.grid(row=1, column=0, columnspan=6, sticky=tk.NSEW)
        self.frame.grid(row=0, column=0, sticky=tk.NSEW)

    def create_bindings(self):
        for keypress in ('<Control-o>', '<Alt-o>'):
            self.parent.bind(keypress, self.open)
        for keypress in ('<Control-q>', '<Alt-q>', '<Escape>'):
            self.parent.bind(keypress, self.quit)
        self.parent.bind('<Alt-f>', lambda *args: self.offsetSpinbox.focus())
        self.parent.bind('<Alt-e>', lambda *args: self.encodingCombobox.focus())
        for variable in (self.offset, self.encoding):
            variable.trace_variable('w', self.show_block)

    def show_block(self, *args):
        self.viewText.delete("1.0", "end")
        if not self.filename:
            return
        with open(self.filename, 'rb') as file:
            try:
                file.seek(self.offset.get(), os.SEEK_SET)
                block = file.read(BLOCK_SIZE)
            except ValueError:  # Empty offsetSpinbox
                return
        rows = [block[i:i + BLOCK_WIDTH]
                for i in range(0, len(block), BLOCK_WIDTH)]
        for row in rows:
            self.show_bytes(row)
            self.show_line(row)
        self.viewText.insert('end', '\n')

    def show_bytes(self, row):
        for byte in row:
            tags = ()
            if byte in b'\t\n\r\v\f':
                tags = ('hexspace', 'graybg')
            elif 0x20 < byte < 0x7F:
                tags = ('ascii',)
            self.viewText.insert('end', '{:02X}'.format(byte), tags)
            self.viewText.insert('end', ' ')
        if len(row) < BLOCK_WIDTH:
            self.viewText.insert('end', ' ' * (BLOCK_WIDTH - len(row)) * 3)

    def show_line(self, row):
        for char in row.decode(self.encoding.get(), errors='replace'):
            tags = ()
            if char in '\u2028\u2029\t\n\r\v\f\uFFFD':
                char = '.'
                tags = ('graybg' if char == '\uFFFD' else 'error')
            elif 0x20 < ord(char) < 0x7F:
                tags = ('ascii',)
            elif not 0x20 <= ord(char) <= 0xFFFF:   # Tcl/Tk limit
                char = "?"
                tags = ('error',)
            self.viewText.insert('end', char, tags)
        self.viewText.insert('end', '\n')

    def open(self, *args):
        self.viewText.delete('1.0', 'end')
        self.offset.set(0)
        filename = filedialog.askopenfilename(title='Open - {}'.format(
                                              APPNAME))
        self._open(filename)

    def _open(self, filename):
        if filename and os.path.exists(filename):
            self.parent.title("{} - {}".format(filename, APPNAME))
            size = os.path.getsize(filename)
            size = (size - BLOCK_SIZE if size > BLOCK_SIZE else
                    size - BLOCK_WIDTH)
            self.offsetSpinbox.config(to=max(size, 0))
            self.filename = filename
            self.show_block()

    def quit(self, event=None):
        self.parent.destroy()


if __name__ == '__main__':
    app = tk.Tk()
    app.title(APPNAME)
    window = MainWindow(app)
    app.protocol("WM_DELETE_WINDOW", window.quit)
    app.resizable(width=False, height=False)
    app.mainloop()
