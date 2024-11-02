# I had to do something... so here we go - MF (Thought it would be great to sign comments with initials so we could blame each other)

import sys
from UI.gui_loader import GUILoader
from UI.si_loader import SILoader

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "-gui":
        gui_loader = GUILoader()
        gui_loader.start_gui()
    else:
        shell_interface = SILoader()
        shell_interface.start_txt()

if __name__ == "__main__":
    main()