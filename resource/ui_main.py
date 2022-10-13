# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 700)
        MainWindow.setMinimumSize(QSize(600, 700))
        MainWindow.setMaximumSize(QSize(600, 700))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.check_all_pushButton = QPushButton(self.centralwidget)
        self.check_all_pushButton.setObjectName(u"check_all_pushButton")
        self.check_all_pushButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.check_all_pushButton)

        self.uncheck_all_pushButton = QPushButton(self.centralwidget)
        self.uncheck_all_pushButton.setObjectName(u"uncheck_all_pushButton")
        self.uncheck_all_pushButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.uncheck_all_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.tableWidget)

        self.save_pushButton = QPushButton(self.centralwidget)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(10)
        self.save_pushButton.setFont(font)

        self.verticalLayout.addWidget(self.save_pushButton)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.check_all_pushButton.setText(QCoreApplication.translate("MainWindow", u"Check all", None))
        self.uncheck_all_pushButton.setText(QCoreApplication.translate("MainWindow", u"Uncheck all", None))
        self.save_pushButton.setText(QCoreApplication.translate("MainWindow", u"Save selected images", None))
    # retranslateUi

