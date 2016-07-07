# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Plotter.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1104, 892)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1104, 26))
        self.menubar.setObjectName("menubar")
        self.menuFormat = QtWidgets.QMenu(self.menubar)
        self.menuFormat.setObjectName("menuFormat")
        self.menuFigure_Width_Format = QtWidgets.QMenu(self.menuFormat)
        self.menuFigure_Width_Format.setObjectName("menuFigure_Width_Format")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionStyle = QtWidgets.QAction(MainWindow)
        self.actionStyle.setObjectName("actionStyle")
        self.actionSingle_Column = QtWidgets.QAction(MainWindow)
        self.actionSingle_Column.setObjectName("actionSingle_Column")
        self.actionDouble_Column = QtWidgets.QAction(MainWindow)
        self.actionDouble_Column.setObjectName("actionDouble_Column")
        self.actionJournal_Styles = QtWidgets.QAction(MainWindow)
        self.actionJournal_Styles.setObjectName("actionJournal_Styles")
        self.actionMacro_Schema = QtWidgets.QAction(MainWindow)
        self.actionMacro_Schema.setObjectName("actionMacro_Schema")
        self.menuFigure_Width_Format.addAction(self.actionSingle_Column)
        self.menuFigure_Width_Format.addAction(self.actionDouble_Column)
        self.menuFormat.addAction(self.actionStyle)
        self.menuFormat.addAction(self.menuFigure_Width_Format.menuAction())
        self.menuFormat.addSeparator()
        self.menuFormat.addAction(self.actionJournal_Styles)
        self.menuFormat.addAction(self.actionMacro_Schema)
        self.menubar.addAction(self.menuFormat.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFormat.setTitle(_translate("MainWindow", "Format"))
        self.menuFigure_Width_Format.setTitle(_translate("MainWindow", "Figure Width Format"))
        self.actionStyle.setText(_translate("MainWindow", "Color Scheme"))
        self.actionSingle_Column.setText(_translate("MainWindow", "Single-Column"))
        self.actionDouble_Column.setText(_translate("MainWindow", "Double-Column"))
        self.actionJournal_Styles.setText(_translate("MainWindow", "Journal Styles"))
        self.actionMacro_Schema.setText(_translate("MainWindow", "Macro Schema"))

