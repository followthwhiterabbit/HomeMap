#!/home/kaan/qt_designs/venv/bin/python3


import sys, os
from PyQt6 import QtWidgets, QMessageBox
import subprocess



from MainWindow import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.setWindowTitle("HomeMap-Open Source Local Network Topology Analyzer")    
        
        self.stacked = self.stackedWidget

        self.setCentralWidget(self.stacked)

        actionInfo = self.actionInfo
        actionVersion = self.actionVersion
        actionQuit = self.actionQuit


        actionInfo.triggered.connect(lambda: self.stacked.setCurrentIndex(1))
        actionVersion.triggered.connect(lambda: self.stacked.setCurrentIndex(0))

        
        self.actionInfo.triggered.connect(self.scan_home_network)
        self.actionInfo.triggered.connect(self.displayProgramInformation)
        self.actionVersion.triggered.connect(self.displayVersionInformation)
        self.actionQuit.triggered.connect(self.QuitApplication)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)



    def scan_home_network(self, checked):

        #return_code = subprocess.Popen(('ls | grep README '),shell=True, stdout=subprocess.PIPE)
        return_code = subprocess.Popen(('ifconfig'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # this returns none, which is wrong 
          
        output, err = return_code.communicate()

        output = output.decode('utf-8').split('\n')


        for i, line in enumerate(output):
            if line.startswith("wlo"):
                print("matched line", line.strip())
                if i + 1 < len(output):
                    ip_line = output[i+1].strip()
                    parts = ip_line.split()
                    if len(parts) >= 2 and parts[0] == "inet":
                        ip = parts[1]
                        #self.lineEdit.setText(ip)  
                        self.label_2.setText(ip)


    def displayProgramInformation(self):

        self.text = """HomeMap software is developed with the purpose of visualizing local home newtork topologies with the help of common network scanning command tools to obtain useful information. You can scan your local network to get useful information about the devices connected to your local gateway as well as to obtain possible Common Vulnerability Exposures and the severity scores of your devices.

Current goals of the software mainly include:

        1 - Scanning end-point devices such as computers, laptops, smartphones, and other IoT devices.
        2-  Developing a dynamic network topology with appropriate visualization tools.
        3 - Trying to enumerate the os, version and common vulnerabilitiy database checkup.
        4 - Finding potential vulnerabilities and severity scores of the devices.
         

        """


        self.label_3.setText(self.text)
    


    def displayVersionInformation(self):

        self.version_text = "Version 0.1.0\n\nThis is the first version of HomeMap software, which is developed to visualize local home network topologies and provide useful information about connected devices. The software is still in development and new features will be added in future versions."



        self.version_label.setText(self.version_text)




    def QuitApplication(self):

        reply = QMessageBox.question(self, 'Window Close', 'Are you sure 'Are you sure you want to close the window?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            print('Application exited')
        else:
            pass







app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()


