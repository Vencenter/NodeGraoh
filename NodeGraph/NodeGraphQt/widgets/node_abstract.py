#!/usr/bin/python
#-*- coding:utf-8 -*-
from PySide import QtGui, QtCore
QtWidgets = QtGui

from .constants import Z_VAL_NODE


class AbstractNodeItem(QtWidgets.QGraphicsItem):#所有查询信息的功能在此实现
    """
    The abstract base class of a node.
    """

    def __init__(self, name='node', parent=None):
        super(AbstractNodeItem, self).__init__(parent)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setZValue(Z_VAL_NODE)
        self.prev_pos = self.pos
        self._properties = {
            'id': hex(id(self)),
            'name': name.strip(),
            'color': (48, 58, 69, 255),
            'border_color': (85, 100, 100, 255),
            'text_color': (255, 255, 255, 180),
            'type': 'AbstractBaseNode',
            'selected': False,
            'disabled': False,
        }
        self._width = 120
        self._height = 80

    def __str__(self):
        return '{}.{}(\'{}\')'.format(
            self.__module__, self.__class__.__name__, self.name)

    def __repr__(self):
        return '{}.{}(\'{}\')'.format(
            self.__module__, self.__class__.__name__, self.name)

    def boundingRect(self):
        return QtCore.QRectF(0.0, 0.0, self._width, self._height)

    def setSelected(self, selected):
        super(AbstractNodeItem, self).setSelected(selected)
        self._properties['selected'] = selected

    def pre_init(self, viewer, pos=None):
        """
        Called before node has been added into the scene.

        Args:
            viewer (NodeGraphQt.widgets.viewer.NodeViewer): main viewer.
            pos (tuple): the cursor pos if node is called with tab search.
        """
        pass

    def post_init(self, viewer, pos=None):
        """
        Called after node has been added into the scene.

        Args:
            viewer (NodeGraphQt.widgets.viewer.NodeViewer): main viewer
            pos (tuple): the cursor pos if node is called with tab search.
        """
        pass

    @property
    def id(self):
        return self._properties['id']

    @id.setter
    def id(self, unique_id=''):
        self._properties['id'] = unique_id

    @property
    def type(self):
        return self._properties['type']

    @type.setter
    def type(self, node_type='NODE'):
        self._properties['type'] = node_type

    @property
    def size(self):
        return self._width, self._height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width=0.0):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height=0.0):
        self._height = height

    @property
    def color(self):
        return self._properties['color']

    @color.setter
    def color(self, color=(200, 0, 0, 255)):
        self._properties['color'] = color

    @property
    def text_color(self):
        return self._properties['text_color']

    @text_color.setter
    def text_color(self, color=(100, 100, 100, 255)):
        self._properties['text_color'] = color

    @property
    def border_color(self):
        return self._properties['border_color']

    @border_color.setter
    def border_color(self, color=(0, 0, 0, 255)):
        self._properties['border_color'] = color

    @property
    def disabled(self):
        return self._properties['disabled']

    @disabled.setter
    def disabled(self, state=False):
        self._properties['disabled'] = state

    @property
    def selected(self):
        return self.isSelected()

    @selected.setter
    def selected(self, selected=False):
        pass
        #self.setSelected(selected)

    @property
    def pos(self):
        return float(self.scenePos().x()), float(self.scenePos().y())

    @pos.setter
    def pos(self, pos=[0.0, 0.0]):
        self.prev_pos = self.scenePos().x(), self.scenePos().y()
        self.setPos(pos[0], pos[1])

    @property
    def name(self):
        return self._properties['name']

    @name.setter
    def name(self, name=''):
        if self.scene():
            viewer = self.scene().viewer()
            name = viewer.get_unique_node_name(name)
        self._properties['name'] = name
        self.setToolTip('node: {}'.format(name))

    @property
    def properties(self):
        """
        Returns:
            dict: {property_name: property_value}
        """
        return self._properties

    def has_property(self, name):
        return name in self._properties.keys()

    def add_property(self, name, value):
        if name in self._properties.keys():
            raise AssertionError('property "{}" already exists!')
        self._properties[name] = value

    def get_property(self, name):
        return self._properties.get(name)

    def set_property(self, name, value):
        class_name = self.__class__.__name__
        if not self._properties.get(name):
            raise AssertionError('{} has no property "{}"'
                                 .format(class_name, name))

        if isinstance(value, type(self._properties[name])):
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                self._properties[name] = value
        else:
            raise TypeError('{} property "{}" has to be a {} type.'
                            .format(class_name, name, value))

    def viewer(self):
        """
        return the main viewer.

        Returns:
            NodeGraphQt.widgets.viewer.NodeViewer: viewer object.
        """
        if self.scene():
            return self.scene().viewer()

    def delete(self):
        """
        delete node item from the scene.
        """
        if self.scene():
            self.scene().removeItem(self)

    def to_dict(self):
        """
        serialize node object to a dict:.

        Returns:
            dict: node id as the key and properties as the values eg.
                {'0x106cf75a8': {
                    'name': 'foo node',
                    'color': (48, 58, 69, 255),
                    'border_color': (85, 100, 100, 255),
                    'text_color': (255, 255, 255, 180),
                    'type': 'com.chantasticvfx.FooNode',
                    'selected': False,
                    'disabled': False,
                    'pos': (0.0, 0.0)
                    }
                }
        """
        serial = {
            self.id: {k: v for k, v in self._properties.items() if k != 'id'}
        }
        serial[self.id]['pos'] = self.pos
        return serial

    def from_dict(self, node_dict):
        """
        deserialize dict to node.

        Args:
            node_dict (dict): serialized node dict.
        """
        for name, value in node_dict.items():
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                self.set_property(name, value)
