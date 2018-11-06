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

class NodeGraph(NodeGraphWidget):
    """
    Example node graph widget.
    """

    def __init__(self, parent=None):
        super(NodeGraph, self).__init__(parent)
        self.setWindowTitle('My Node Graph')

        self.setGeometry(230,20,1100,800)
        NODES_TO_REGISTER = [
            custom_node.CustomNode,
            menu_node.MenuNode,
            simple_nodes.FooNode,
            simple_nodes.BarNode,
            text_input_node.TextNode,
            newscene_node.NewSceneNode,
            createHierachy_node.SceneHierachyNode]
       
        for node in NODES_TO_REGISTER:
            self.register_node(node)

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
        #self.setDragEnabled(True)
        self._middle=NodeGraph()
        self.setAutoScroll(False)
        for d in Node_name:
            item = QtGui.QTreeWidgetItem(self, [d])
            item.setIcon(0,QtGui.QIcon('example/example_icon.png'))
    
    def showdir(self, item):
        path=self.currentItem().text(0)
        self._middle.show()
        itemname=path
        newname=path.replace(' ','')
        create_node = self._middle.create_node(
            'com.chantasticvfx.'+newname, name=itemname)
        create_node.set_pos(-287.0, 141.0)

class Mainwindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.setWindowTitle('My_Node_Graph')
        self.resize(1000, 800)
        self.initUI()
    def initUI(self):
        self._tree=TreeView()
        self._tree.setStyleSheet("TreeView{background-color:gray;}")
        Layt=QtGui.QHBoxLayout()
        Layt.addWidget(self._tree)
        self.setLayout(Layt)
        self._tree.itemDoubleClicked.connect(self._tree.showdir)
        self.show()
        self.setGeometry(20,20,200,800)

        

    
             

    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    graph = Mainwindow()
    
    graph.show()
    app.exec_()
