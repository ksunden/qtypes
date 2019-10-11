__all__ = ["InputTable"]


import os
import collections
from PySide2 import QtWidgets, QtGui

from ._spin_box import DoubleSpinBox


# size notes for input table
#   all rows have height of exactly 25
#   all rows have width of exactly 150
#   total widget width is 300


class InputTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setMargin(5)
        self.setFixedWidth(300)
        self.row_number = 0
        self.controls = []
        self._objs = {}

    def __getattr__(self):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __setitem__(self, value):
        raise NotImplementedError

    def append(self, obj, label=None):
        if label is None:
            label = obj.name
        # type
        if obj is None:
            _type = "heading"
            self._append_heading(label)
        else:
            _type = obj.qtype
            setattr(self, obj.name, obj)
            getattr(self, f"_append_{_type}")(label, obj)
            self._objs[obj.name] = obj

    def _append_heading(self, label):
        row_layout = self._get_row_layout(label)
        row_layout.addStretch(1)

    def _append_number(self, label, obj):
        row_layout = self._get_row_layout(label)
        # layout
        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(QtWidgets.QHBoxLayout())
        layout = container_widget.layout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        # control
        control = DoubleSpinBox()
        if obj.disabled:
            control.setDisabled(True)
        obj.give_control(control)
        layout.addWidget(control)
        control.setFixedWidth(150)
        # units combobox
        if not obj.units_kind == None:
            control.setMinimumWidth(150 - 55)
            control.setMaximumWidth(150 - 55)
            units = QtWidgets.QComboBox()
            units.setMinimumWidth(50)
            units.setMaximumWidth(50)
            layout.addWidget(units)
            obj.give_units_combo(units)
        # finish
        self.controls.append(container_widget)
        row_layout.addWidget(container_widget)

    def _append_string(self, name, global_object):
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.layout().addWidget(heading, self.row_number, 0)
        # control
        control = QtWidgets.QLineEdit()
        control.setMinimumWidth(self.width_input)
        control.setMaximumWidth(self.width_input)
        if global_object.disabled:
            control.setDisabled(True)
        global_object.give_control(control)
        # finish
        self.layout().addWidget(control, self.row_number, 1)
        self.controls.append(control)
        self.row_number += 1

    def _append_enum(self, name, global_object):
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        heading.setStyleSheet(StyleSheet)
        self.layout().addWidget(heading, self.row_number, 0)
        # control
        control = QtWidgets.QComboBox()
        control.setMinimumWidth(self.width_input)
        control.setMaximumWidth(self.width_input)
        global_object.give_control(control)
        # finish
        self.layout().addWidget(control, self.row_number, 1)
        self.controls.append(control)
        self.row_number += 1

    def _append_bool(self, name, global_object):
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.layout().addWidget(heading, self.row_number, 0)
        # control
        if global_object.display:
            control = Led()
        else:
            control = QtWidgets.QCheckBox()
        global_object.give_control(control)
        # finish
        self.layout().addWidget(control, self.row_number, 1)
        self.controls.append(control)
        self.row_number += 1

    def _append_filepath(self, name, global_object):
        raise NotImplementedError
        # heading
        heading = QtWidgets.QLabel(name)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        StyleSheet = "QLabel{color: custom_color; font: 14px;}".replace(
            "custom_color", colors[foreground]
        )
        heading.setStyleSheet(StyleSheet)
        self.layout().addWidget(heading, self.row_number, 0)
        # layout
        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(QtWidgets.QHBoxLayout())
        layout = container_widget.layout()
        layout.setMargin(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        # push button
        load_button = QtWidgets.QPushButton("Load")
        load_button.setMinimumHeight(20)
        load_button.setMaximumHeight(20)
        load_button.setMinimumWidth(40)
        load_button.setMaximumWidth(40)
        layout.addWidget(load_button)
        global_object.give_button(load_button)
        # display
        display = QtWidgets.QLineEdit()
        # display.setDisabled(True)
        display.setReadOnly(True)
        display.setMinimumWidth(self.width_input - 45)
        display.setMaximumWidth(self.width_input - 45)
        layout.addWidget(display)
        global_object.give_control(display)
        # finish
        self.layout().addWidget(container_widget, self.row_number, 1)
        self.controls.append(container_widget)
        self.row_number += 1

    def extend(self):
        raise NotImplementedError

    def _get_row_layout(self, label):
        # create layout
        layout = QtWidgets.QHBoxLayout()
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # add heading
        heading = QtWidgets.QLabel(label)
        heading.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        heading.setFixedHeight(25)
        heading.setFixedWidth(150)
        heading.setMargin(0)
        layout.addWidget(heading)
        # create widget
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        widget.setFixedHeight(25)
        widget.setStyleSheet("background-color: red")
        self.layout().addWidget(widget, self.row_number)
        # finish
        self.row_number += 1
        return layout

    def insert(self):
        raise NotImplementedError

    def keys(self):
        return self._objs.keys()

    def len(self):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def values(self):
        return self._objs.values()
