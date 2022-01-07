# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from .main_window import Ui_MainWindow
from data_base.hakaton_db import data_base


class MainWindow_super(Ui_MainWindow, QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.data = data_base('../data_base/main_db.db')

    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        self.pushButton_new_coach.clicked.connect(self.add_coach)
        self.pushButton_coach_delete.clicked.connect(self.delete_coach)
        self.comboBox_coach.activated.connect(self.combobox_coach_action)
        self.pushButton_item_new.clicked.connect(self.add_item)
        self.pushButton_item_delete.clicked.connect(self.delete_item)
        self.comboBox_item.activated.connect(self.combobox_item_action)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Q:
            print('heh')
        event.accept()

    def retranslateUi(self, MainWindow):
        Ui_MainWindow.retranslateUi(self, MainWindow)
        print(self.data.return_list_names('coach'))
        self.reboot_list('coach')
        self.reboot_list('tools')

    def reboot_list(self, name):
        if name == 'coach':
            self.comboBox_coach.clear()
            for i in self.data.return_list_names(name):
                self.comboBox_coach.addItem(i)
        elif name == 'tools':
            self.comboBox_item.clear()
            for i in self.data.return_list_names(name):
                print(i)
                self.comboBox_item.addItem(i)

    def delete_coach(self):
        self.data.delete_info('coach', ['name'], [self.lineEdit_coach_name.text()])
        self.reboot_list('coach')

    def add_coach(self):
        if self.lineEdit_coach_name.text() != '' and self.lineEdit_coach_price != '' and self.lineEdit_coach_id != '':
            self.data.add_coach(self.lineEdit_coach_name.text(), self.lineEdit_coach_price.text(),
                                self.lineEdit_coach_id.text())
        self.reboot_list('coach')

    def add_item(self):
        if self.lineEdit_item_name.text() != '' and self.lineEdit_item_price != '':
            self.data.add_tools(self.lineEdit_item_name.text(), self.lineEdit_item_price.text())
        self.reboot_list('tools')

    def delete_item(self):
        self.data.delete_info('tools', ['name'], [self.lineEdit_item_name.text()])
        self.reboot_list('tools')

    def combobox_item_action(self):
        row = self.data.return_row('tools', self.comboBox_item.currentText())
        self.lineEdit_item_name.setText(row[0])
        self.lineEdit_item_price.setText(str(row[1]))

    def combobox_coach_action(self):
        row = self.data.return_row('coach', self.comboBox_coach.currentText())
        self.lineEdit_coach_name.setText(row[0])
        self.lineEdit_coach_price.setText(str(row[1]))
        self.lineEdit_coach_id.setText(str(row[2]))
