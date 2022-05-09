from qtpy import QtWidgets, QtGui, QtCore


class Widget(QtWidgets.QSpinBox):
    def __init__(self, model, parent):
        super().__init__(parent=parent)
        self.editingFinished.connect(self.on_editing_finished)
        # wire into model
        self.model = model
        self.model.updated_connect(self.on_updated)
        self.on_updated(model.get())

    def on_editing_finished(self):
        self.model.set({"value": self.value()}, from_widget=True)

    def on_updated(self, data):
        self.setValue(data["value"])
        self.setDisabled(data["disabled"])
