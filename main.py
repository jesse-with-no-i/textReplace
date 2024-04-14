import sys

from guiApp import mainWindow
from PyQt5.QtWidgets import QApplication
from replacer import Replacer
import consoleApp


def runGuiApp():
    app = QApplication(sys.argv)
    # create a window
    window = mainWindow()
    window.show()
    # configure window exit function
    sys.exit(app.exec_())

def main():
    # BEGIN BLACK BOX TEST

    # newReplacer = Replacer(infile="my_text.txt")
    #
    # newReplacer.add_replacement("SIGMA", "Σ")
    # newReplacer.add_replacement("DELTA", "δ")
    # newReplacer.add_replacement("GAMMA", "Ⲅ")
    # newReplacer.add_replacement("ELEMENT_OF", "∊")
    # newReplacer.add_replacement("SUBSET_OF", "⊆")
    #
    # newReplacer.replace_text()

    # END BLACK BOX TEST

    # uncomment for console application
    # consoleApp.run()

    # uncomment for GUI application
    runGuiApp()


if __name__ == '__main__':
    main()

