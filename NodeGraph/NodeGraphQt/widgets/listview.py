#-*- coding:utf-8 -*-
import sys
import os,json
from PySide import QtGui, QtCore
QtWidgets = QtGui
class ListView(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ListView,self).__init__(parent=parent)
        self.setWindowTitle(u"参数面板")
        self.setAcceptDrops(True)
        self.resize(260,600)

