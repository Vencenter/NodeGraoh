#-*- coding:utf-8 -*-
import re,os,json
from PySide import QtGui, QtCore
QtWidgets = QtGui
from .constants import VIEWER_BG_COLOR, VIEWER_GRID_OVERLAY, VIEWER_GRID_COLOR
import listview
class NodeScene(QtWidgets.QGraphicsScene):

    def __init__(self, parent=None):
        super(NodeScene, self).__init__(parent)
        self.background_color = VIEWER_BG_COLOR
        self.grid = VIEWER_GRID_OVERLAY
        self.grid_color = VIEWER_GRID_COLOR

    def __repr__(self):
        return '{}.{}(\'{}\')'.format(self.__module__,
                                      self.__class__.__name__,
                                      self.viewer())

    def _draw_grid(self, painter, rect, pen, grid_size):
        lines = []
        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)
        x = left
        while x < rect.right():
            x += grid_size
            lines.append(QtCore.QLineF(x, rect.top(), x, rect.bottom()))
        y = top
        while y < rect.bottom():
            y += grid_size
            lines.append(QtCore.QLineF(rect.left(), y, rect.right(), y))
        painter.setPen(pen)
        painter.drawLines(lines)

    def drawBackground(self, painter, rect):
        painter.save()
        color = QtGui.QColor(*self._bg_color)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, False)
        painter.setBrush(color)
        painter.drawRect(rect.normalized())
        if not self._grid:
            return
        grid_size = 20
        zoom = self.viewer().get_zoom()
        color = QtGui.QColor(*self.grid_color)
        grid_alpha = 8
        if zoom > -4:
            color.setAlpha(grid_alpha)
            pen = QtGui.QPen(color, 0.65)
            self._draw_grid(painter, rect, pen, grid_size)
        if zoom < 0:
            color.setAlpha(grid_alpha * (0.05 * (zoom * -1) + 1.0))
        else:
            color.setAlpha(grid_alpha * 1.1)
        pen = QtGui.QPen(color, 0.5)
        self._draw_grid(painter, rect, pen, grid_size * 8)
        painter.restore()
        
        #*************************************************************************************
        #*************************************************************************************
        #*************************************************************************************
    def mouseDoubleClickEvent(self, event):#增加鼠标双击事件,并添加参数面板的布局等信息。#*****范围内为增加的代码
        selected_nodes = self.viewer().selected_nodes()
        if selected_nodes==[]:
            return 0
        nodeName= str(selected_nodes).split("\'")
        nodeName= nodeName[1]


        #nodeName=str(selected_nodes[0]).replace("NodeGraphQt.widgets.node_base.NodeItem(\'","")
        #nodeName=nodeName.replace("\')","")
    
        
        if "Text Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/Text.json"
            #print nodeName
        elif "Foo Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/Foo.json"
            #print nodeName
        elif "Bar Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/Bar.json"
            #print nodeName
        elif "Menu Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/menu.json"
            #print nodeName
        elif "Hierachy Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/Hierachy.json"
            #print nodeName
        elif "My Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/custom.json"
            #print nodeName
        elif "Newscene Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/newScene.json"
            #print nodeName
        elif "Input text Node" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/textInput.json"
            #print nodeName
        elif "Backdrop" in nodeName:
            path_json="NodeGraphQt/nodes/jsonFile/backDrop.json"
            #print nodeName

        #print nodeName
        self._list=listview.ListView()
        self._list.setStyleSheet("ListView{background-color:gray;}")
        titleLabel=QtGui.QLabel(nodeName,self._list)
        titleLabel.setGeometry(QtCore.QRect(100, 0, 100, 20)) 
                                 
        if os.path.isfile(path_json):
            with open(path_json) as file:
                dict_all = json.loads(file.read())
            #print dict_all['parameters panel']
            param_len=len(dict_all['parameters panel'])
            self.labelList=dict_all['parameters panel']
            self.paramlList=dict_all['parameters panel']
            
            for i in range(param_len):
                self.labelList[i]=QtGui.QLabel(dict_all['parameters panel'][i],self._list)
                self.labelList[i].setGeometry(QtCore.QRect(10, 20, 70, i*60+35))
                if i==0:
                    self.paramlList[i]=QtGui.QLineEdit(str(self.grid_color),self._list)
                    self.paramlList[i].setGeometry(QtCore.QRect(90, 30*i+25, 150, 22))
                elif i==1:
                    self.paramlList[i]=QtGui.QLineEdit(str(self.background_color),self._list)
                    self.paramlList[i].setGeometry(QtCore.QRect(90, 30*i+25, 150, 22))
                elif i==2:
                    self.paramlList[i]=QtGui.QLineEdit(self._list)
                    self.paramlList[i].setGeometry(QtCore.QRect(90, 30*i+25, 150, 22))
                elif i==3:
                    self.paramlList[i]=QtGui.QLineEdit("0",self._list)
                    self.paramlList[i].setGeometry(QtCore.QRect(90, 30*i+25, 150, 22))
                elif i==4:
                    self.paramlList[i]=QtGui.QLineEdit("0",self._list)
                    self.paramlList[i].setStyleSheet("ListView{background-color:pink;}")
                    self.paramlList[i].setGeometry(QtCore.QRect(90, 30*i+25, 150, 22))
                else:
                    self.paramlList[i]=QtGui.QLineEdit(self._list)
                    self.paramlList[i].setGeometry(QtCore.QRect(90, 30*i+25, 150, 22))
                    

        
        
        useButton=QtGui.QPushButton('use',self._list)
        useButton.setGeometry(QtCore.QRect(150, 280, 80, 40))
        useButton.clicked.connect(self.changeEvent)
        self._list.show()
        
    def changeEvent(self):
        color=str(self.paramlList[0].text())
        print color
        color1=str(self.paramlList[1].text())
        print color1
        color2=str(self.paramlList[2].text())
        print color2
    #*******************************************
    def dragEnterEvent(self, event):
        #print('graphics view drag enter')
        data = event.mimeData().hasFormat('application/x-item')
        print data
        if (event.mimeData().hasFormat('application/x-item')):
            event.acceptProposedAction()
            print('accepted')
        else:
            event.ignore() 
    def dropEvent(self, event): 
        #print('graphics view drop')
        event.acceptProposedAction()
        data = event.mimeData()
        urls = data.urls()
        print data
        if ( urls and urls[0].scheme() == 'file' ):
            filepath = str(urls[0].path())[1:]
            filepath=filepath.decode('utf-8')
            print filepath
        
    def mousePressEvent(self, event):
        selected_nodes = self.viewer().selected_nodes()
        if self.viewer():
            self.viewer().sceneMousePressEvent(event)
        super(NodeScene, self).mousePressEvent(event)
        keep_selection = any([
            event.button() == QtCore.Qt.MiddleButton,
            event.button() == QtCore.Qt.RightButton,
            event.modifiers() == QtCore.Qt.AltModifier
        ])
        if keep_selection:
            for node in selected_nodes:
                node.setSelected(True)

    def mouseMoveEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseMoveEvent(event)
        super(NodeScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.viewer():
            self.viewer().sceneMouseReleaseEvent(event)
        super(NodeScene, self).mouseReleaseEvent(event)

    def viewer(self):
        return self.views()[0] if self.views() else None

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, mode=True):
        self._grid = mode

    @property
    def grid_color(self):
        return self._grid_color

    @grid_color.setter
    def grid_color(self, color=(0, 0, 0)):
        self._grid_color = color

    @property
    def background_color(self):
        return self._bg_color

    @background_color.setter
    def background_color(self, color=(0, 0, 0, 0)):
        self._bg_color = color
