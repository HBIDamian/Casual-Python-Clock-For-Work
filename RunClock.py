import os
import sys
import time
import warnings
import webbrowser
warnings.filterwarnings("ignore", category=UserWarning)
# Check if PyQt5 is installed, display a warning if not
try:
    from PyQt5.QtWidgets import (
        QApplication, QLabel, QMainWindow, QAction, QMessageBox, QColorDialog, QMenu
    )
    from PyQt5.QtCore import (
        Qt, QTimer
    )
    from PyQt5.QtGui import (
        QFont, QFontDatabase, QFontMetrics, QColor
    )
except ImportError:
    print("PyQt5 is not installed. Please install it using 'pip install PyQt5'")
    sys.exit(1)

# Define the main application window for the digital clock
class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initial settings
        self.default_font_size = 200
        self.current_font_size = self.default_font_size
        self.min_font_size = 50
        self.max_font_size = 480
        self.is_fullscreen = False
        self.foreground_color = 'white'
        self.background_color = 'black'
        self.menubar_visible = True
        self.setWindowTitle('Digital Clock')
        self.initUI()

    # Initialize UI components and settings
    def initUI(self):
        self.loadCustomFont()
        self.createLabel()
        self.createTimer()
        self.setInitialWindowSize()
        self.createMenuBar()
        self.show()

    # Load custom font for the digital clock
    def loadCustomFont(self):
        font_path = os.path.join(os.path.dirname(__file__), './Assets/Font/seven-leds.ttf')
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print("Failed to load font")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    # Create the main label for displaying the time
    def createLabel(self):
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(self.geometry())
        self.setCentralWidget(self.label)
        self.updateFontSize()
        self.updateTime()

    # Create and start a timer to update the time display every second
    def createTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(250)

    # Set the initial window size based on the font metrics
    def setInitialWindowSize(self):
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)

    # Create the menu bar with settings and help options
    def createMenuBar(self):
        self.menubar = self.menuBar()
        settings_menu = self.menubar.addMenu('Settings')
        colours_menu = QMenu('Colours', self)
        bg_color_action = QAction('Background Colour', self)
        bg_color_action.triggered.connect(self.set_background_color)
        colours_menu.addAction(bg_color_action)
        fg_color_action = QAction('Foreground Colour', self)
        fg_color_action.triggered.connect(self.set_foreground_color)
        colours_menu.addAction(fg_color_action)
        settings_menu.addMenu(colours_menu)
        # Add "Presets" menu to Colors
        presets_menu = QMenu('Presets', self)
        presets_menu.addAction('Black on White').triggered.connect(lambda: self.setPresetColors('white', 'black'))
        presets_menu.addAction('White on Black').triggered.connect(lambda: self.setPresetColors('black', 'white'))
        presets_menu.addAction('Red on Black').triggered.connect(lambda: self.setPresetColors('black', 'red'))
        presets_menu.addAction('Green on Black').triggered.connect(lambda: self.setPresetColors('black', 'green'))
        presets_menu.addAction('Blue on Black').triggered.connect(lambda: self.setPresetColors('black', 'blue'))
        colours_menu.addMenu(presets_menu)
        help_menu = self.menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        help_action = QAction('Shortcuts', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    # Display the about message box
    def show_about(self):
        about_message = (
            "Idle Digital Clock (using Python)\n\n"
            "A simple digital clock application\n"
            "Created by HBIDamian"
        )
        about_message_box = QMessageBox()
        about_message_box.setWindowTitle("About")
        about_message_box.setText(about_message)
        about_message_box.setInformativeText("For more information, visit the GitHub repository.")
        about_message_box.setIcon(QMessageBox.Information)
        github_button = about_message_box.addButton("GitHub", QMessageBox.ActionRole)
        github_button.clicked.connect(self.open_github)
        about_shortcuts_button = about_message_box.addButton("Shortcuts", QMessageBox.ActionRole)
        about_shortcuts_button.clicked.connect(self.show_help)
        about_message_box.exec_()

    # Open the GitHub repository page
    def open_github(self):
        webbrowser.open("https://github.com/HBIDamian/Casual-Python-Clock-For-Work")

    # Display the keyboard shortcuts help message
    def show_help(self):
        help_message = (
            "Keyboard Shortcuts:\n\n"
            "F, F11\t Toggle Fullscreen\n"
            "-, _\t Decrease Font Size\n"
            "+, =\t Increase Font Size\n"
            "0, F5\t Reset Font Size\n"
            "/, ?, F1 \t Show Help\n"
            "M, T\t Toggle Menubar\n"
            "Settings > Colours > Background Colour: Change Background Colour\n"
            "Settings > Colours > Foreground Colour: Change Foreground Colour"
        )
        QMessageBox.information(self, "Help", help_message)

    # Update the displayed time
    def updateTime(self):
        self.label.setText(time.strftime("%H:%M:%S"))

    # Handle key press events for shortcuts
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F or event.key() == Qt.Key_F11:
            self.toggleFullscreen()
        elif event.key() in (Qt.Key_Minus, Qt.Key_Underscore):
            self.changeFontSize(-5)
        elif event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            self.changeFontSize(5)
        elif event.key() in (Qt.Key_0, Qt.Key_F5):
            self.resetFontSize()
        elif event.key() in (Qt.Key_Slash, Qt.Key_Question, Qt.Key_F1):
            self.show_help()
        elif event.key() in (Qt.Key_M, Qt.Key_T):
            self.toggleMenubar()

    # Toggle between fullscreen and normal window size
    def toggleFullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
        else:
            self.showFullScreen()
            self.updateWindowSizeFullscreen()
        self.is_fullscreen = not self.is_fullscreen

    # Toggle the visibility of the menubar
    def toggleMenubar(self):
        if self.menubar_visible:
            self.menubar.hide()
        else:
            self.menubar.show()
        self.menubar_visible = not self.menubar_visible

    # Change the font size by a specified delta
    def changeFontSize(self, delta):
        self.current_font_size += delta
        if self.current_font_size < self.min_font_size:
            self.current_font_size = self.min_font_size
        elif self.current_font_size > self.max_font_size:
            self.current_font_size = self.max_font_size
        self.updateFontSize()

    # Reset the font size to the default size
    def resetFontSize(self):
        self.current_font_size = self.default_font_size
        self.updateFontSize()

    # Update the font size and other style properties of the label
    def updateFontSize(self):
        self.label.setStyleSheet(
            f"font-family: '{self.font_family}'; "
            f"font-size: {self.current_font_size}px; "
            f"letter-spacing: .2em; "
            f"color: {self.foreground_color}; "
            f"background-color: {self.background_color};"
        )
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)

    # Update the window size and position when in fullscreen mode
    def updateWindowSizeFullscreen(self):
        screen_rect = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_rect)

    # Function to set preset colors
    def setPresetColors(self, bg_color, fg_color):
        self.background_color = bg_color
        self.foreground_color = fg_color
        self.updateFontSize()

    # Open a color dialog to set the background color
    def set_background_color(self):
        bg_color = QColorDialog.getColor(QColor(self.background_color), self, "Select Background Colour")
        if bg_color.isValid():
            self.background_color = bg_color.name()
            self.updateFontSize()

    # Open a color dialog to set the foreground color
    def set_foreground_color(self):
        fg_color = QColorDialog.getColor(QColor(self.foreground_color), self, "Select Foreground Colour")
        if fg_color.isValid():
            self.foreground_color = fg_color.name()
            self.updateFontSize()

    # Handle mouse wheel events to change font size
    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.changeFontSize(5)
        else:
            self.changeFontSize(-5)

    # Handle middle mouse button click to reset font size
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.resetFontSize()

    # Handle double click events to toggle fullscreen
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggleFullscreen()

    # Resize label and maintain alignment on window resize
    def resizeEvent(self, event):
        self.label.setGeometry(self.rect())
        self.label.setAlignment(Qt.AlignCenter)
        super().resizeEvent(event)

# Main entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Clock()
    sys.exit(app.exec_())
