#-*- coding:utf-8 -*-
import sys
import os,json
from PySide import QtGui, QtCore
QtWidgets = QtGui
from NodeGraphQt import NodeGraphWidget
from NodeGraphQt import Node
from NodeGraphQt.nodes import simple_nodes
from NodeGraphQt.nodes import text_input_node
from NodeGraphQt.nodes import menu_node
from NodeGraphQt.nodes import custom_node
from NodeGraphQt.nodes import newscene_node
from NodeGraphQt.nodes import createHierachy_node
from NodeGraphQt.widgets import listview


reload(sys)
sys.setdefaultencoding("utf-8")

listp=['']
class NodeGraph(NodeGraphWidget):
    """
    Example node graph widget.
    """

    def __init__(self, parent=None):
        super(NodeGraph, self).__init__(parent)
        self.setWindowTitle('My Node Graph')
        self.resize(1100, 800)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

class TreeView(QtGui.QTreeWidget):
    def __init__(self,parent=None):
        super(TreeView,self).__init__(parent=parent)
        self.setHeaderLabels(['Node_Create'])
        Node_name=["Text Node","Foo Node","Bar Node","Menu Node","New Scene Node",'Scene Hierachy Node',"Custom Node"]
        #self.setAcceptDrops(True)
        self.setDragEnabled(True)
       
        self.setAutoScroll(False)
        for d in Node_name:
            item = QtGui.QTreeWidgetItem(self, [d])
            item.setIcon(0,QtGui.QIcon('example/example_icon.png'))
    
    def showdir(self, item):
        path=self.currentItem().text(0)
        listp.append(path)
        return path  

class Mainwindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setWindowTitle('My_Node_Graph')
        self.resize(1000, 800)
        self.initUI()
    def initUI(self):
        self._tree=TreeView()
        self._tree.setStyleSheet("TreeView{background-color:gray;}")
        self._middle=NodeGraph()
        self._list=listview.ListView()
        self._list.setStyleSheet("ListView{background-color:gray;}")
        
        mainSplitter=QtGui.QSplitter(QtCore.Qt.Horizontal)
        
        mainSplitter.setOpaqueResize(1)
        mainSplitter.addWidget(self._tree)
        mainSplitter.addWidget(self._middle)
        
        
        Layt=QtGui.QHBoxLayout()
        Layt.addWidget(mainSplitter)
        
        self.setLayout(Layt)
        
        self._tree.itemDoubleClicked.connect(self._tree.showdir)
        self._tree.itemDoubleClicked.connect(self.getName)
        
        self.show()

        NODES_TO_REGISTER = [
            custom_node.CustomNode,
            menu_node.MenuNode,
            simple_nodes.FooNode,
            simple_nodes.BarNode,
            text_input_node.TextNode,
            newscene_node.NewSceneNode,
            createHierachy_node.SceneHierachyNode]
       
        for node in NODES_TO_REGISTER:
            self._middle.register_node(node)
    def getName(self):
        path=listp[-1]#print item name
        self._middle.show()
        itemname=path
        newname=path.replace(' ','')
        create_node = self._middle.create_node(
            'com.chantasticvfx.'+newname, name=itemname)
        create_node.set_pos(-287.0, 141.0)

    
    
            

                
       
               

    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = Mainwindow()
    
    graph.show()
    app.exec_()
