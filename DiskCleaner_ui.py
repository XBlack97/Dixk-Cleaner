# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DiskCleaner.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(594, 341)
        #MainWindow.setStyleSheet("background-color: rgb(81, 81, 81);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("background-color: rgb(189, 189, 189);\n"
"alternate-background-color: rgb(44, 44, 44);\n"
"border-color: rgb(185, 185, 185);")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.Temp_Tab = QtWidgets.QWidget()
        self.Temp_Tab.setObjectName("Temp_Tab")
        self.tabWidget.addTab(self.Temp_Tab, "")
        self.Duplicate_Tab = QtWidgets.QWidget()
        self.Duplicate_Tab.setObjectName("Duplicate_Tab")
        self.tabWidget.addTab(self.Duplicate_Tab, "")

        self.UnUsed_Tab = QtWidgets.QWidget()
        self.UnUsed_Tab.setObjectName("UnUsed_Tab")
        self.tabWidget.addTab(self.UnUsed_Tab, "")


        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Disk Cleaner"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Temp_Tab), _translate("MainWindow", "Temp Files"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.Temp_Tab), _translate("MainWindow",
                                                                                       "Temporary files..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Duplicate_Tab), _translate("MainWindow",
                                                                                         "Duplicate files"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.Duplicate_Tab), _translate("MainWindow",
                                                                                            "Duplicate Files..."))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.UnUsed_Tab), _translate("MainWindow", "Dormant files"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.UnUsed_Tab),
                                     _translate("MainWindow", "Unused Files for a peeriod of time..."))

