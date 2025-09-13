#!/home/kaan/qt_designs/venv/bin/python3

import sys, os, math, nmap
from PyQt6 import QtWidgets

import subprocess

from MainWindow import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # an empty set to keep track of the network modules of the end device self.

        #self.ifconfig_units = set([])  
        #self.flags_info = []
        self.hardware_flags_dict = {}
        self.hardware_mtu_dict = {}
        self.hardware_mac_dict = {}
        self.hardware_bcast_dict = {}
        self.hardware_ipv4_dict = {}
        self.hardware_ipv6_dict = {}
        self.hardware_nm_dict = {}
        
        # number of hosts in the local network
        self.num_of_hosts = 0
        self.percent_value = 0

        # icons 
        self.home_pc_label = QtWidgets.QLabel(self.widget)
        self.home_pc_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        # label should be in the center of self.widget
        self.home_pc_label.setGeometry(QtCore.QRect(125, 125, 64, 64)) # x,y,width,height

       
        self.home_pc_label_icon = QtGui.QPixmap("icons/some_other/monitor.png")

        self.home_pc_label.setPixmap(self.home_pc_label_icon)

        self.visible = True
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.toggle_icon) 
        self.timer.start(700) 
        
        self.setWindowTitle("HomeMap-Open Source Local Network Topology Analyzer")    
        
        self.stacked = self.stackedWidget

        self.setCentralWidget(self.stacked)
        
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(0)

        actionInfo = self.actionInfo
        actionVersion = self.actionVersion
        actionQuit = self.actionQuit

        actionMenu = self.menuHome.addAction("Home Menu")

        
        actionInfo.setIcon(QtGui.QIcon("icons/info/information.png"))
        actionVersion.setIcon(QtGui.QIcon("icons/system/version.png"))
        actionMenu.setIcon(QtGui.QIcon("icons/some_other/home.png"))

        actionMenu.triggered.connect(lambda: self.stacked.setCurrentIndex(2))
        actionMenu.triggered.connect(lambda: self.tabs.clear()) # clear the table when switched to home page
        actionInfo.triggered.connect(lambda: self.stacked.setCurrentIndex(1))
        actionInfo.triggered.connect(lambda: self.tabs.clear()) # clear the table when switched to info page
        actionVersion.triggered.connect(lambda: self.stacked.setCurrentIndex(0))
        actionVersion.triggered.connect(lambda: self.tabs.clear())

         
        
        self.tabs = self.tabWidget
        self.tabs_2 = self.tabWidget_2


        
        # we need to clear the tabs when we open home page 
        # when the home page is opened, we need to clear the tabs

        
        self.ifconfig_button.clicked.connect(self.scan_home_network)
        self.topology_button.clicked.connect(self.nmap_search)
        self.topology_button.clicked.connect(self.paintEvent)
        self.clearpaint_button.clicked.connect(self.clear_paint)


        self.ifconfig_button.setToolTip('Obtain information about the network interface of this computer')
        self.topology_button.setToolTip('Scan the local network and find the number of hosts connected to the local gateway')

        #self.actionInfo.triggered.connect(self.scan_home_network)
        self.actionInfo.triggered.connect(self.displayProgramInformation)
        self.actionVersion.triggered.connect(self.displayVersionInformation)
        self.actionQuit.triggered.connect(self.QuitApplication)


        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)



    def toggle_icon(self):
        if self.visible:
            self.home_pc_label.clear()
        else:
            self.home_pc_label.setPixmap(self.home_pc_label_icon)
        self.visible = not self.visible



    def scan_home_network(self, checked):
        # clear the interface set before
        self.hardware_flags_dict.clear()
        self.hardware_mtu_dict.clear()
        self.hardware_mac_dict.clear()

        #return_code = subprocess.Popen(('ls | grep README '),shell=True, stdout=subprocess.PIPE)
        return_code = subprocess.Popen(('ifconfig'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # this returns none, which is wrong 
          
        output, err = return_code.communicate()

        output = output.decode('utf-8')
        
        devices = output.strip().split("\n\n")

        for i, dev in enumerate(devices, 1):
            lines = dev.splitlines() # this takes lines of every splitted hardware of our computer 
            first_line = lines[0] 
            name = first_line.split(":")[0] 
            
            flags = first_line.split()[1].split("=")[1] # takes the flags 
            mtu = first_line.split()[3] # we take the maximum_transmission_unit   

            #self.flags_info.append(flags)
            #self.ifconfig_units.add(name)
           
            # we need to map from key to the strings dict[key-device_name] --> string(flag)
            self.hardware_flags_dict[name] = flags
            self.hardware_mtu_dict[name] = mtu            
            

        #self.displayIfconfigUnits()     
        self.progressBar.setValue(50)
        
        #for indv in self.hardware_mac_dict:
        #    print(self.hardware_mac_dict)

        for i, dev in enumerate(devices, 1):
            lines = dev.splitlines()
            first_line = lines[0]
            name = first_line.split(":")[0]
            
            self.hardware_mac_dict[name] = ''
            self.hardware_bcast_dict[name] = ''
            self.hardware_ipv4_dict[name] = ''
            self.hardware_ipv6_dict[name] = ''
            self.hardware_nm_dict[name] = ''


            self.progressBar.setValue(75)
            for line in lines:
                parts = line.split()
                if parts and parts[0] == 'ether':
                    self.hardware_mac_dict[name] = parts[1]
                    #break # no need to check for further lines for this device 
                for part in parts:
                    if part == 'broadcast':
                        index_part = parts.index(part)
                        self.hardware_bcast_dict[name] = parts[index_part+1]
                    if part == 'inet':
                        index_part = parts.index(part)
                        self.hardware_ipv4_dict[name] = parts[index_part+1]
                    if part == 'inet6':
                        index_part = parts.index(part)
                        self.hardware_ipv6_dict[name] = parts[index_part+1]
                    if part == 'netmask':
                        index_part = parts.index(part)
                        self.hardware_nm_dict[name] = parts[index_part+1]

        self.progressBar.setValue(100)
        #print(self.hardware_mac_dict)


        self.displayIfconfigUnits()     
    


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
        
        self.version_label.setText("Software Version")
        self.version_number.setText("V0.1")




    def displayIfconfigUnits(self):
        self.tabs.clear()
        for unit in self.hardware_flags_dict:
            tab = QtWidgets.QWidget()
            tab.setObjectName(unit)
            tab_layout = QtWidgets.QHBoxLayout(tab)
            #tab_label = QtWidgets.QLabel(f"Information for {unit}")
            #tab_label.setObjectName(f"{unit}_label")
            #tab_layout.addWidget(tab_label)
            self.tabs.addTab(tab, unit)
             
            table = QtWidgets.QTableWidget(tab) # every tab is our parent widget
            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
             
            table.setColumnCount(2) 
            table.setRowCount(7)

            table.setHorizontalHeaderLabels(["Property", "Value"])
            
            #set tooltip for the table items one by one 
            inet_table_item = QtWidgets.QTableWidgetItem("inet")
            inet_table_item.setToolTip("IPv4 Address of the device")
            inet_table_item.setFlags(inet_table_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable) 
            table.setItem(0, 0, inet_table_item) 
            table.resizeColumnsToContents()
            
            net_mask_item = QtWidgets.QTableWidgetItem("Inet4 NetMask")
            net_mask_item.setToolTip("NetMask of Ipv4 address") 
            net_mask_item.setFlags(net_mask_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable) 
            table.setItem(1, 0, net_mask_item)
            table.resizeColumnsToContents()


            inet6_table_item = QtWidgets.QTableWidgetItem("inet6")
            inet6_table_item.setToolTip("IpV6 Address of the hardware interface")
            inet6_table_item.setFlags(inet6_table_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(2, 0, inet6_table_item)
            table.resizeColumnsToContents()

            mac_item = QtWidgets.QTableWidgetItem("mac address") 
            mac_item.setToolTip("Mac address of the interface")
            mac_item.setFlags(mac_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(3, 0, mac_item)
            table.resizeColumnsToContents()

            broadcast_item = QtWidgets.QTableWidgetItem("broadcast address")
            broadcast_item.setToolTip("Broadcast address of the interface")
            broadcast_item.setFlags(broadcast_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(4, 0, broadcast_item)
            table.resizeColumnsToContents()

             
            flags_item = QtWidgets.QTableWidgetItem("Flags")
            flags_item.setToolTip("Shows useful information about the realtime condition of the interface")
            flags_item.setFlags(flags_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(5, 0, flags_item)
            table.resizeColumnsToContents()
           

            mtu_item = QtWidgets.QTableWidgetItem("Maximum Transmission Unit")
            mtu_item.setToolTip("Gives useful information about the amount of transmission size in bytes") 
            mtu_item.setFlags(mtu_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(6, 0, mtu_item)
            table.resizeColumnsToContents()

        

            table_ip =  QtWidgets.QTableWidgetItem(self.hardware_ipv4_dict[unit])
            table.setItem(0, 1, table_ip)
            table_ip.setFlags(table_ip.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            if table_ip.text() == '':
                table_ip.setBackground(QtGui.QColor("gray"))   
            else:
                table_ip.setBackground(QtGui.QColor("green"))

            table.resizeColumnsToContents()
            
            
            table_nm = QtWidgets.QTableWidgetItem(self.hardware_nm_dict[unit])
            table_nm.setFlags(table_nm.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(1, 1, table_nm)  
            if table_nm.text() == '':
                table_nm.setBackground(QtGui.QColor("gray"))
            else:
                table_nm.setBackground(QtGui.QColor("green"))

            table.resizeColumnsToContents()



            table_ipv6 = QtWidgets.QTableWidgetItem(self.hardware_ipv6_dict[unit])
            table_ipv6.setFlags(table_ipv6.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(2, 1, table_ipv6)  
            if table_ipv6.text() == '':
                table_ipv6.setBackground(QtGui.QColor("gray"))
            else:
                table_ipv6.setBackground(QtGui.QColor("green"))


            table.resizeColumnsToContents()
            
            table_mac_dict = QtWidgets.QTableWidgetItem(self.hardware_mac_dict[unit])
            table_mac_dict.setFlags(table_mac_dict.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(3, 1, table_mac_dict)
            if table_mac_dict.text() == '': 
                table_mac_dict.setBackground(QtGui.QColor("gray"))
            else:
                table_mac_dict.setBackground(QtGui.QColor("green"))

            table.resizeColumnsToContents()

            table_bcast_dict = QtWidgets.QTableWidgetItem(self.hardware_bcast_dict[unit])  
            table_bcast_dict.setFlags(table_bcast_dict.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(4, 1, table_bcast_dict)  
            if table_bcast_dict.text() == '':
                table_bcast_dict.setBackground(QtGui.QColor("gray"))
            else: 
                table_bcast_dict.setBackground(QtGui.QColor("green"))

            table.resizeColumnsToContents()

            table_flags = QtWidgets.QTableWidgetItem(self.hardware_flags_dict[unit])
            table_flags.setFlags(table_flags.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(5, 1, table_flags)
            if table_flags.text() == '':
                table_flags.setBackground(QtGui.QColor("gray"))
            else:
                table_flags.setBackground(QtGui.QColor("green"))

            table.resizeColumnsToContents()
            
            table_mtu = QtWidgets.QTableWidgetItem(self.hardware_mtu_dict[unit])
            table_mtu.setFlags(table_mtu.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            table.setItem(6, 1, table_mtu)
            if table_mtu.text() == '':
                table_mtu.setBackground(QtGui.QColor("gray"))
            else:
                table_mtu.setBackground(QtGui.QColor("green"))
 


            table.resizeColumnsToContents()
            
            tab_layout.addWidget(table)
            # Set the tab as the current tab
            self.tabs.setCurrentWidget(tab)







    
    # this function will take number of items from the nmap search
    # we also need to clean the paint event so that it does not draw lines on other pages

    def paintEvent(self, event):
        
        # this lines should not show up other than menu page 
        if self.stacked.currentIndex() != 2:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtCore.Qt.GlobalColor.green)
        painter.setBrush(QtCore.Qt.GlobalColor.white)
        #painter.drawLine(150, 190, 200, 250)

        # cx and cy will be the cx and cy of the logo 
        cx, cy  =  200, 266
        radius = 100
        num_lines = self.num_of_hosts - 1 # we should not count our own device apparently

   

        for i in range(num_lines):
            angle = i * (360 / num_lines)  # degrees
            rad = math.radians(angle)
            x = cx + radius * math.cos(rad)
            y = cy - radius * math.sin(rad)  # minus because Qt y-axis is downward
            painter.drawLine(cx, cy, int(x), int(y))
             

    
    # this function will clean the paint when we press clear button or switch to other pages
    def clear_paint(self, event):
        self.num_of_hosts = 0
        self.repaint()
        self.progressBar.setValue(0)
        #self.update()
        #self.paintEvent(None)




    # we need to have a widget to be able to make nmap searches and use nmap library
    # count the number of hosts in the local network
    def nmap_search(self):
        nm = nmap.PortScanner()
        #nm.scan('192.168.0.0/24', '22-443')

        self.progressBar_2.setValue(0)
        nm.scan('192.168.0.0/24', arguments='-sn', sudo=True)  
        
        for host in nm.all_hosts():
            #print('--------------------------------------------')
            #print('Host : %s (%s)' % (host, nm[host].hostname()))
            #print('State : %s' % nm[host].state())
            #for proto in nm[host].all_protocols():
                #print('--------')
                #print('Protocol : %s' % proto)


                #lport = nm[host][proto].keys()
                #sorted(lport)
                #for port in lport:
                    #print('port: %s\tstate: %s' % (port, nm[host][proto][port]['state']))
        
            self.num_of_hosts += 1
        
        self.percent_value = int(100 / self.num_of_hosts)
        

        self.tabs_2.clear()
        for host in nm.all_hosts():
            i = 1
            # this will use the second tab widget which is QTabWidget_2
            # we will create a new tab for every host
            tab = QtWidgets.QWidget()
            tab.setObjectName(host)
            tab_layout = QtWidgets.QHBoxLayout(tab)
            #tab_label = QtWidgets.QLabel(f"Information for {host}")
            #tab_label.setObjectName(f"{host}_label")
            #tab_layout.addWidget(tab_label)
            self.tabs_2.addTab(tab, host)
            

            table_hosts = QtWidgets.QTableWidget(tab) # every tab is our parent widget
            table_hosts.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

            table_hosts.setColumnCount(2)
            table_hosts.setRowCount(4)

            table_hosts.setHorizontalHeaderLabels(["Prop..", "Val"])

            # set tooltip for the table items one by one
            hostname_item = QtWidgets.QTableWidgetItem("Hostname")
            hostname_item.setToolTip("Hostname of the device")
            table_hosts.setItem(0, 0, hostname_item)
            table_hosts.resizeColumnsToContents()

            hostname_value = QtWidgets.QTableWidgetItem(nm[host].hostname())
            table_hosts.setItem(0, 1, hostname_value)
            hostname_value.setToolTip("Hostname of the device")
            table_hosts.resizeColumnsToContents()

            state_item = QtWidgets.QTableWidgetItem("State")
            state_item.setToolTip("State of the device")
            table_hosts.setItem(1, 0, state_item)
            table_hosts.resizeColumnsToContents()


            state_value = QtWidgets.QTableWidgetItem(nm[host].state())
            table_hosts.setItem(1, 1, state_value)
            state_value.setToolTip("State of the device")
            table_hosts.resizeColumnsToContents()

            protocol_item = QtWidgets.QTableWidgetItem("Protocols")
            protocol_item.setToolTip("Protocols of the device")
            table_hosts.setItem(2, 0, protocol_item)
            table_hosts.resizeColumnsToContents()

            protocols = ', '.join(nm[host].all_protocols())
            protocol_value = QtWidgets.QTableWidgetItem(protocols)
            table_hosts.setItem(2, 1, protocol_value)
            protocol_value.setToolTip("Protocols of the device")
            table_hosts.resizeColumnsToContents()


            ports_item = QtWidgets.QTableWidgetItem("Open Ports")
            ports_item.setToolTip("Open Ports of the device")
            table_hosts.setItem(3, 0, ports_item)
            table_hosts.resizeColumnsToContents()


            open_ports = []
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    if nm[host][proto][port]['state'] == 'open':
                        open_ports.append(f"{port}/{proto}")



            table_hosts.resizeColumnsToContents()
            
            tab_layout.addWidget(table_hosts)
            # Set the tab as the current tab
            self.tabs.setCurrentWidget(tab)



            i += 1 
            self.progressBar_2.setValue(i * self.percent_value)


        self.progressBar_2.setValue(100)




    def QuitApplication(self):

        reply = QtWidgets.QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?', QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.close()
            print('Application exited')
        else:
            pass







app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()


