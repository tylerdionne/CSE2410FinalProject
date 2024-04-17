from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextBrowser, QMessageBox
from PyQt5.QtCore import QTimer
from ColorOutputBrowser import ColorOutputBrowser
from pwn import process


##################################################################################################################################

class PwnDbgGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.pwndbgprocess = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('pwndbg')
        self.resize(800, 600)
        
        # binary file input
        self.binaryinput = QLineEdit(self)
        self.binaryinput.setPlaceholderText("Enter binary name")
        
        # function name input 
        self.functioninput = QLineEdit(self)
        self.functioninput.setPlaceholderText("Enter function name")

        # user input/payload
        self.userinput = QLineEdit(self)
        self.userinput.setPlaceholderText("Enter payload")
        
        # button to set breakpoint at function name
        self.breakpointbutton = QPushButton('Set Breakpoint', self)
        self.breakpointbutton.clicked.connect(self.setbreakpoint)
        
        # button to disassemble function name
        self.disassemblebutton = QPushButton('Disassemble', self)
        self.disassemblebutton.clicked.connect(self.disassm)
        
        # button to run the program
        self.runbutton = QPushButton('Run', self)
        self.runbutton.clicked.connect(self.run)
            
        # button to continue
        self.continuebutton = QPushButton('Continue', self)
        self.continuebutton.clicked.connect(self.cont)

        # button to init/start pwndbg 
        self.startbutton = QPushButton('Start pwndbg', self)
        self.startbutton.clicked.connect(self.startpwndbg)

        # button to send the users input to program
        self.sendinputbutton = QPushButton('Send payload', self)
        self.sendinputbutton.clicked.connect(self.sendinput)
        
        # button to exit pwndbg an close the window
        self.exitbutton = QPushButton('Exit', self)
        self.exitbutton.clicked.connect(self.close)
        
        # use ColorOutputBrowser class to print output in color
        self.outputarea = ColorOutputBrowser(self)
        self.outputarea.setReadOnly(True)
        
        # add the input boxes to gui
        vbox = QVBoxLayout()
        vbox.addWidget(self.binaryinput)
        vbox.addWidget(self.functioninput)
        vbox.addWidget(self.userinput)

        # make a layout for the gui with buttons an input boxes
        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.startbutton)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.breakpointbutton)
        hbox1.addWidget(self.disassemblebutton)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.runbutton)
        hbox2.addWidget(self.continuebutton)
        hbox2.addWidget(self.sendinputbutton)
        
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.outputarea)
        vbox.addWidget(self.exitbutton)
        
        self.setLayout(vbox)
    
    ##################################################################################################################################

    def startpwndbg(self):
        binaryname = self.binaryinput.text()

        # need a binary name before we set a breakpoint
        if not binaryname:
            QMessageBox.warning(self, "Input Error", "Please enter a binary name first.")
            return

        # if already started print error return
        if self.pwndbgprocess:
            QMessageBox.warning(self, "Input Error", "Already started.")
            return

        # to start pwndbg $ pwndbg ./{binaryfile}
        try:
            self.pwndbgprocess = process(["pwndbg", f"./{binaryname}"])
            print("Starting...")
            output = ""
            while True:
            	line = self.pwndbgprocess.recvline(timeout=5).decode()
            	if line == "":
            		print("Start complete")
            		break
            	output += line
            self.outputarea.append(output)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Timed out while starting pwndbg...")
       
    ##################################################################################################################################
    
    def setbreakpoint(self):
        binaryname = self.binaryinput.text()
        functionname = self.functioninput.text()

        # need a binary name before we set a breakpoint
        if not binaryname:
            QMessageBox.warning(self, "Input Error", "Please enter a binary name first.")
            return

        # need a function name before we set a breakpoint
        if not functionname:
            QMessageBox.warning(self, "Input Error", "Please enter a function name first.")
            return

        # pwndbg have to be started before set break point
        if not self.pwndbgprocess:
            QMessageBox.warning(self, "Input Error", "pwndbg not stated.")
            return

        # $ pwndbg> break {functionname}
        try:
            self.pwndbgprocess.sendline(f"break {functionname}")
            output = ""
            while True:
            	line = self.pwndbgprocess.recvline(timeout=5).decode()
            	if line == "":
            		print("Breakpoint set")
            		break
            	output += line
            self.outputarea.append(output)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Timed out while setting breakpoint...")

    ##################################################################################################################################
    
    def disassm(self):
        binaryname = self.binaryinput.text()
        functionname = self.functioninput.text()

        # need a binary name before we set a breakpoint
        if not binaryname:
            QMessageBox.warning(self, "Input Error", "Please enter a binary name first.")
            return

        # need a function name before we set a breakpoint
        if not functionname:
            QMessageBox.warning(self, "Input Error", "Please enter a function name first.")
            return

        # pwndbg have to be started before set break point
        if not self.pwndbgprocess:
            QMessageBox.warning(self, "Input Error", "pwndbg not stated.")
            return

        # $ pwndbg> disassemble {functionname}
        try:
            self.pwndbgprocess.sendline(f"disassemble {functionname}")
            output = ""
            while True:
            	line = self.pwndbgprocess.recvline(timeout=10).decode()
            	if line == "":
            		print("Disassembly complete")
            		break
            	output += line
            self.outputarea.append(output)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Timed out while disassembling...")

    ##################################################################################################################################
    
    def run(self):
        binaryname = self.binaryinput.text()
        functionname = self.functioninput.text()

        # need a binary name before we set a breakpoint
        if not binaryname:
            QMessageBox.warning(self, "Input Error", "Please enter a binary name first.")
            return

        # pwndbg have to be started before set break point
        if not self.pwndbgprocess:
            QMessageBox.warning(self, "Input Error", "pwndbg not stated.")
            return

        # $ pwndbg> r
        try:
            self.pwndbgprocess.sendline("r")
            output = ""
            while True:
            	line = self.pwndbgprocess.recvline(timeout=5).decode()
            	if line == "":
            		print("Running...")
            		break
            	output += line
            self.outputarea.append(output)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Timed out while running...")

    ##################################################################################################################################
    
    def cont(self):
        binaryname = self.binaryinput.text()
        functionname = self.functioninput.text()

        # need a binary name before we set a breakpoint
        if not binaryname:
            QMessageBox.warning(self, "Input Error", "Please enter a binary name first.")
            return

        # pwndbg have to be started before set break point
        if not self.pwndbgprocess:
            QMessageBox.warning(self, "Input Error", "pwndbg not stated.")
            return

        # $ pwndbg> c
        try:
            self.pwndbgprocess.sendline("c")
            output = ""
            while True:
            	line = self.pwndbgprocess.recvline(timeout=5).decode()
            	if line == "":
            		print("Continuing...")
            		break
            	output += line
            self.outputarea.append(output)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Timed out while setting continuing...")

    ##################################################################################################################################
        
    def sendinput(self):
        binaryname = self.binaryinput.text()
        functionname = self.functioninput.text()
        userin = self.userinput.text()

        # need a binary name before we set a breakpoint
        if not binaryname:
            QMessageBox.warning(self, "Input Error", "Please enter a binary name first.")
            return

        # pwndbg have to be started before set break point
        if not self.pwndbgprocess:
            QMessageBox.warning(self, "Input Error", "pwndbg not stated.")
            return

        # need input to send input
        if not self.userinput:
            QMessageBox.warning(self, "Input Error", "No payload supplied")
            return

        # send user input to the program
        # if try to send payload when program not expecting, will just print error to the screen wont crash
        try:
            self.pwndbgprocess.sendline(f"{userin}")
            output = ""
            while True:
                line = self.pwndbgprocess.recvline(timeout=5).decode()
                if line == "":
                    print("Payload sent")
                    break
                output += line
            self.outputarea.append(output)
        except Exception as e:
            QMessageBox.warning(self, "Error", "Timed out while sending payload...")

##################################################################################################################################


