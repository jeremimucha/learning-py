#! python3


class Wizard:

    def __init__(self, src, rootdir):
        self._choices = []
        self._rootdir = rootdir
        self._src = src

    def preferences(self, command):
        self._choices.append(command)

    def execute(self):
        for choice in self._choices:
            if list(choice.values())[0]:
                print("Copying binaries --", self._src, ' to ',
                self._rootdir)
            else:
                print("No Operation")

if __name__ == '__main__':
    ## Client code
    wizard = Wizard('python35.gzip', '/usr/bin/')
    ## User chooses to install python only
    wizard.preferences({'python': True})
    wizard.preferences({'java': False})
    wizard.execute()
