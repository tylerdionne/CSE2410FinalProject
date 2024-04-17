from PyQt5.QtWidgets import QTextBrowser
from ansi2html import Ansi2HTMLConverter

##################################################################################################################################

class ColorOutputBrowser(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.converter = Ansi2HTMLConverter()

    def append(self, text):
        # want to convert ansi escape codes to html to get output in color
        html = self.converter.convert(text, full=True)
        super().append(html)

##################################################################################################################################
