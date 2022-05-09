__all__ = ["TreeWidget"]


import sys
import pathlib

from qtpy import QtWidgets, QtGui, QtCore

from .._base import Base
from .._styles import styles
from ._bool import Widget as BoolWidget
from ._null import Widget as NullWidget
from ._button import Widget as ButtonWidget
from ._enum import Widget as EnumWidget
from ._float import Widget as FloatWidget
from ._integer import Widget as IntegerWidget
from ._string import Widget as StringWidget


__here__ = pathlib.Path(__file__).parent


widgets = dict()
widgets["bool"] = BoolWidget
widgets["null"] = NullWidget
widgets["button"] = ButtonWidget
widgets["enum"] = EnumWidget
widgets["float"] = FloatWidget
widgets["integer"] = IntegerWidget
widgets["string"] = StringWidget


class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, model, *, include_root=True):
        width = 250
        super().__init__(parent=None, width=width)
        self.setColumnCount(2)
        self.setHeaderLabels(["", ""])
        sheets = list(styles["tomorrow-night"].values())
        self.setStyleSheet("".join(sheets))
        self.setColumnWidth(width // 2, width // 2)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.model = model
        self.include_root = include_root
        self.children = []
        self.model.restructured_connect(self._build_tree)
        self._build_tree()

    def __getitem__(self, index):
        if index < 0:
            index = self.topLevelItemCount() + index
        return self.topLevelItem(index)

    def append(self, item):
        self.addTopLevelItem(item)
        if isinstance(item, Base):
            widget = item._widget
            widget.setParent(self)
            self.setItemWidget(item, 1, widget)
            self.children.append(item)

    def _build_tree(self):
        self.clear()

        def make_item(model):
            item = QtWidgets.QTreeWidgetItem([model.get()["label"], ""])
            widget = widgets[model.qtype](parent=self, model=model)
            return item, widget

        def make_widget(parent, model):
            item, widget = make_item(model)
            parent.addChild(item)
            self.setItemWidget(item, 1, widget)
            for child in model.children:
                make_widget(item, child)

        if not self.include_root:
            model = self.model.children
        else:
            model = self.model
        # top level items
        for m in model:
            item, widget = make_item(m)
            self.addTopLevelItem(item)
            self.children.append(item)
            self.setItemWidget(item, 1, widget)
            for child in m.children:
                make_widget(item, child)

    def clear(self):
        while self.children:
            child = self.children.pop(0)
            self.takeTopLevelItem(0)

    def insert(self, index, item):
        if index < 0:
            index += self.topLevelItemCount()
        if index < 0:
            index = 0
        if index > self.topLevelItemCount():
            index = self.topLevelItemCount()
        self.insertTopLevelItem(index, item)
        if isinstance(item, Base):
            widget = item._widget
            widget.setParent(self)
            self.setItemWidget(item, 1, widget)
            self.children.insert(index, item)
