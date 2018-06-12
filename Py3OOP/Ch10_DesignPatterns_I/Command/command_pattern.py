'''
The command pattern is used to interface the client code calls to the
receiver object that manages its own internal state when the command is executed
A common example is actions in a GUI - command Invokers are menu bars,
a keyboard shortcut, toolbar icons etc. Actions that actually occur are
Exit, Save, Copy - these are implementations of CommandInterface which are
later used on Receivers.
'''
import sys


#Receivers
class Window:
    def exit(self):
        sys.exit(0)


class Document:
    def __init__(self, filename):
        self.filename = filename
        self.contents = "This file cannot be modified"

    def save(self):
        with open(self.filename, 'w') as file:
            file.write(self.contents)


# Invoker classes
# commands arent set on initialization - they're added later dynamically
# (this isn't necessary, just an example; could be set on init)
class ToolbarButton:
    def __init__(self, name, iconname):
        self.name = name
        self.iconname = iconname

    def click(self):
        self.command.execute()


class MenuItem:
    def __init__(self, menu_name, menuitem_name):
        self.menu = menu_name
        self.item = menuitem_name

    def click(self):
        self.command.execute()


class KeyboardShortcut:
    def __init__(self, key, modifier):
        self.key = key
        self.modifier = modifier

    def keypress(self):
        self.command.execute()


# Commands
class SaveCommand:
    def __init__(self, document):
        self.document = document

    def execute(self):
        self.document.save()


class ExitCommand:
    def __init__(self, window):
        self.window = window

    def execute(self):
        self.window.exit()


if __name__ == '__main__':
    window = Window()
    document = Document('a_document.txt')
    save = SaveCommand(document)
    exit = ExitCommand(window)

    save_button = ToolbarButton('save', 'save.png')
    save_button.command = save
    save_keystroke = KeyboardShortcut('s', 'ctrl')
    save_keystroke.command = save
    exit_menu = MenuItem('File', 'Exit')
    exit_menu.command = exit
