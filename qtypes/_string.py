__all__ = ["String"]


from ._base import Base


class String(Base):
    qtype = "string"

    def __init__(self, initial_value="", *args, **kwargs):
        super().__init__(initial_value=initial_value, *args, **kwargs)
        self.type = "string"

    def give_control(self, control_widget):
        self.widget = control_widget
        # fill out items
        self.widget.setText(str(self.value.read()))
        # connect signals and slots
        self.updated.connect(lambda: self.widget.setText(self.value.read()))
        self.widget.editingFinished.connect(lambda: self.write(str(self.widget.text())))
        self.widget.setToolTip(self.tool_tip)
        self.has_widget = True
