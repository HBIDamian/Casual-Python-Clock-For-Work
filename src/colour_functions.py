from PyQt5.QtWidgets import QColorDialog

def set_background_color(self):
    bg_color = QColorDialog.getColor(self.background_color, self, "Select Background Colour")
    if bg_color.isValid():
        self.background_color = bg_color.name()
        self.updateFontSize()

def set_foreground_color(self):
    fg_color = QColorDialog.getColor(self.foreground_color, self, "Select Foreground Colour")
    if fg_color.isValid():
        self.foreground_color = fg_color.name()
        self.updateFontSize()

def set_preset_colors(self, bg_color, fg_color):
    self.background_color = bg_color
    self.foreground_color = fg_color
    self.updateFontSize()
