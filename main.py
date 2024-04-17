import sys
import time
from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PwnDbgGUI import PwnDbgGUI

##################################################################################################################################

def main():
    app = QApplication(sys.argv)
    
    # get pwndbg logo found online (make sure in CWD)
    splashpix = QPixmap('logo.png') 
    splash = QSplashScreen(splashpix, Qt.WindowStaysOnTopHint)
    
    # make the fake loading bar
    progressbar = QProgressBar(splash)
    progressbar.setGeometry(560, 400, 200, 200)
    progressbar.setValue(0)

    splash.show()
    
    # simulate loading with sleep()
    for i in range(101):
        progressbar.setValue(i)
        time.sleep(0.02)  
        app.processEvents()
    
    window = PwnDbgGUI()
    # get rid of logo window once delay is done
    QTimer.singleShot(2000, splash.close)
    # show main window after the logo screen done
    QTimer.singleShot(2000, window.show)
    
    sys.exit(app.exec_())

##################################################################################################################################

main()