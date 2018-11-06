#-*- coding:utf-8 -*-
import re,os,json,pickle
from PySide import QtGui, QtCore
QtWidgets = QtGui
from .constants import VIEWER_BG_COLOR, VIEWER_GRID_OVERLAY, VIEWER_GRID_COLOR
import listview
from ..base.node_vendor import NodeVendor
from ..base.node_plugin import NodePlugin
from ..interfaces.node import Backdrop
from .viewer import NodeViewer
from ..base.serializer import SessionSerializer, SessionLoader
from .node_base import NodeItem

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
        self._viewer=self.viewer()
        selected_nodes = self._viewer.selected_nodes()#获取选择节点的实例对象item list
        if selected_nodes==[]:
            return 0
        node_type=selected_nodes[0].type
        NodeInstance = NodeVendor.create_node_instance(node_type)
        self.nodeInstance=NodeInstance()
        self.nodeInstance.set_item(selected_nodes[0])
        #print 'scene get:',(self.nodeInstance)#获取选择节点的实例对象

        #print selected_nodes[0]
        
        
        nodeName= selected_nodes[0].name
        #返回节点名
        #print selected_nodes[0].name
        if nodeName=='Backdrop':
            return 0
        
        
        #print node #获取选择节点的实例对象item
        
      
        


        #**********************************************
        #**********************************************
        #**********************************************
        #***************获取各种属性信息*****************
        #**********************************************
        #**********************************************
        
        '''
        print 'name',t.name
        print 'id',t.id
        print 'hash',t.__hash__()
        print 'properties',t.properties
        
        print 'size',t.size
        print 'text_color',t.text_color
        print 'color',t.color
        print 'border_color',t.border_color
        print 'viewer',t.viewer
        print 'type',t.type
        print 'selected',t.selected
        print 'disabled',t.disabled
        print 'pos',t.pos
        print 'x_pos',t.pos[0]
        print 'y_pos',t.pos[1]
        print 'width',t.width
        print 'height',t.height
        print 'icon',selected_nodes[0].icon
        print 'inputs',selected_nodes[0].inputs
        print 'outputs',selected_nodes[0].outputs'''
        
        #**********************************************
        #**********************************************
        #****************获取各种属性信息****************
        #**********************************************
        #**********************************************
        filename=filter(str.isalpha, str(nodeName))
        path_json="NodeGraphQt/nodes/jsonFile/"+filename+'.json'
        if not os.path.isfile(path_json):
            path_json="NodeGraphQt/nodes/jsonFile/other.json"
    

        self._list=listview.ListView()
        self._list.setStyleSheet("ListView{background-color:gray;}")
        titleLabel=QtGui.QLabel(nodeName,self._list)
        titleLabel.setGeometry(QtCore.QRect(100, 0, 120, 20)) 
                                 
        if os.path.isfile(path_json):
            with open(path_json) as file:
                dict_all = json.loads(file.read())
            #print dict_all['parameters panel']
            self.param_len=len(dict_all['parameters panel'])
            self.labelList=dict_all['parameters panel']
            self.paramlList=dict_all['parameters panel']
            if '(' in str(selected_nodes[0].color):
                color=str(selected_nodes[0].color).replace(', 255)','')
                color=color.replace('(','')
            elif '[' in str(selected_nodes[0].color) :
                color=str(selected_nodes[0].color).replace(', 255]','')
                color=color.replace('[','')
            else:
                print 'unkonw error!'
            for i in range(self.param_len):
                self.labelList[i]=QtGui.QLabel(dict_all['parameters panel'][i],self._list)
                self.labelList[i].setGeometry(QtCore.QRect(10, 20, 100, i*60+35))
                if i==1:
                    self.paramlList[i]=QtGui.QLineEdit(color,self._list)
                    self.paramlList[i].setGeometry(QtCore.QRect(105, 30*i+25, 150, 22))
                else:
                    self.paramlList[i]=QtGui.QLineEdit((""),self._list)
                    self.paramlList[i].setGeometry(QtCore.QRect(105, 30*i+25, 150, 22))
 
        
        useButton=QtGui.QPushButton('use',self._list)
        useButton.setGeometry(QtCore.QRect(150, 280, 80, 40))
        useButton.clicked.connect(self.changeEvent)
        self._list.show()
    def changeEvent(self):
        name=self.paramlList[0].text()
        if name!="":
            try:
                self.nodeInstance.set_name(name)
            except:
                self.Message=QtGui.QMessageBox()
                self.Message.information(self.Message,u"提示界面","name")       
            
        color=self.paramlList[1].text()
        if color!="":
            try:
                if int(color.split(',')[0])<0 or int(color.split(',')[0])>255 \
                   or int(color.split(',')[1])<0 or int(color.split(',')[1])>255\
                   or int(color.split(',')[2])<0 or int(color.split(',')[2])>255:
                    self.Message=QtGui.QMessageBox()
                    self.Message.information(self.Message,u"提示界面",u"r,g,b in [0-255]")
                else:
                    self.nodeInstance.set_color(int(color.split(',')[0]),int(color.split(',')[1]),int(color.split(',')[2]))
            except :
                self.Message=QtGui.QMessageBox()
                self.Message.information(self.Message,u"提示界面",u"参数：r,g,b")
        text_input=self.paramlList[2].text()
        if (text_input)!="":
            try:
                self.nodeInstance.add_text_input(text_input.split(',')[0],text_input.split(',')[1],text_input.split(',')[2])
            except :
                self.Message=QtGui.QMessageBox()
                self.Message.information(self.Message,u"提示界面",u"参数：name,label,text")
        combo_menu=self.paramlList[3].text()
        if (combo_menu)!="":
            try:
                self.nodeInstance.add_combo_menu(combo_menu.split(',')[0],combo_menu.split(',')[1],combo_menu.split(',')[2])
            except :
                self.Message=QtGui.QMessageBox()
                self.Message.information(self.Message,u"提示界面",u"参数：name,label,item")
        addinput=self.paramlList[4].text()
        if len(addinput)!=0 and addinput!='':
            try:
                self.nodeInstance.add_input(addinput)
            except:
                self.Message=QtGui.QMessageBox()
                self.Message.information(self.Message,u"提示界面",u"参数：name")
        addoutput=self.paramlList[5].text()
        if len(addoutput)!=0 and addoutput!='':
            try:
                self.nodeInstance.add_output(addoutput)
            except:
                self.Message=QtGui.QMessageBox()
                self.Message.information(self.Message,u"提示界面",u"参数：name")

       
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
        if ( urls and urls[0].scheme() == 'file' ):
            filepath = str(urls[0].path())[1:]
            filepath=filepath.decode('utf-8')
        
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
