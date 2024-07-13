import os
import sys
import time
import warnings
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QAction, QMessageBox, QColorDialog, QMenu
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QFontMetrics, QColor

warnings.filterwarnings("ignore", category=UserWarning)

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
        # Disable and hide window maximize button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        
        self.setWindowTitle('Digital Clock')
        self.initUI()

    def initUI(self):
        # Initialize UI components
        self.loadCustomFont()
        self.createLabel()
        self.createTimer()
        self.setInitialWindowSize()
        self.createMenuBar()
        self.show()

    def loadCustomFont(self):
        # Load custom font
        font_path = os.path.join(os.path.dirname(__file__), './Assets/Font/seven-leds.ttf')
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print("Failed to load font")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    def createLabel(self):
        # Create main label for displaying time
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(self.geometry())
        self.setCentralWidget(self.label)
        self.updateFontSize()
        self.updateTime()

    def createTimer(self):
        # Create timer to update time display
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(250)

    def setInitialWindowSize(self):
        # Set initial window size based on font metrics
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)

    def createMenuBar(self):
        # Create menu bar with actions and menus
        self.menubar = self.menuBar()
        settings_menu = self.menubar.addMenu('Settings')
        colours_menu = QMenu('Colours', self)
        bg_color_action = QAction('Background Colour', self)
        bg_color_action.triggered.connect(self.set_background_color)
        colours_menu.addAction(bg_color_action)
        fg_color_action = QAction('Foreground Colour', self)
        fg_color_action.triggered.connect(self.set_foreground_color)
        colours_menu.addAction(fg_color_action)
        colours_menu.addSeparator()
        settings_menu.addMenu(colours_menu)

        presets_menu = QMenu('Presets', self)
        # Adding preset actions to change colours
        presets_menu.addAction('Swap Colours').triggered.connect(lambda: self.setPresetColors(self.foreground_color, self.background_color))
        presets_menu.addAction('Random').triggered.connect(lambda: self.setPresetColors('#' + os.urandom(6).hex(), '#' + os.urandom(6).hex()))
        presets_menu.addSeparator()

        presets_dark_menu = QMenu('Dark Themes', self)
        presets_light_menu = QMenu('Light Themes', self)

        presets_dark_menu.addAction('Dark Mode').triggered.connect(lambda: self.setPresetColors('#121212', '#f0f0f0'))
        presets_dark_menu.addAction('White on Black').triggered.connect(lambda: self.setPresetColors('black', 'white'))
        presets_dark_menu.addAction('Red on Black').triggered.connect(lambda: self.setPresetColors('black', 'red'))
        presets_dark_menu.addAction('Dark Green on Black').triggered.connect(lambda: self.setPresetColors('black', 'green'))
        presets_dark_menu.addAction('Dark Blue on Black').triggered.connect(lambda: self.setPresetColors('black', 'blue'))

        presets_light_menu.addAction('Sky Blue').triggered.connect(lambda: self.setPresetColors('#55aaff', '#aaffff'))
        presets_light_menu.addAction('Black on White').triggered.connect(lambda: self.setPresetColors('white', 'black'))
        presets_light_menu.addAction('Light Mode').triggered.connect(lambda: self.setPresetColors('#f0f0f0', '#121212'))
        presets_light_menu.addAction('Black on White').triggered.connect(lambda: self.setPresetColors('white', 'black'))
        
        presets_menu.addMenu(presets_light_menu)
        presets_menu.addMenu(presets_dark_menu)

        colours_menu.addMenu(presets_menu)

        help_menu = self.menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        help_action = QAction('Shortcuts', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def show_about(self):
        # Display about message box
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

    def open_github(self):
        # Open GitHub repository in default web browser
        webbrowser.open("https://github.com/HBIDamian/Casual-Python-Clock-For-Work")

    def show_help(self):
        # Display keyboard shortcuts help message
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

    def updateTime(self):
        # Update time displayed on the label
        self.label.setText(time.strftime("%H:%M:%S"))

    def keyPressEvent(self, event):
        # Handle key press events
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
            self.menubar.setVisible(not self.menubar.isVisible())
        elif event.key() == Qt.Key_Escape:
            if self.is_fullscreen:
                self.toggleFullscreen()
                

    def toggleFullscreen(self):
        # Toggle fullscreen mode
        if self.is_fullscreen:
            self.showNormal()
            self.updateWindowSizeNormal()
            self.menubar.setVisible(True)  # Show menu bar when exiting fullscreen
        else:
            self.showFullScreen()
            self.updateWindowSizeFullscreen()
            self.menubar.setVisible(False)  # Hide menu bar when entering fullscreen
        self.is_fullscreen = not self.is_fullscreen

    def changeFontSize(self, delta):
        # Change font size by delta
        self.current_font_size += delta
        if self.current_font_size < self.min_font_size:
            self.current_font_size = self.min_font_size
        elif self.current_font_size > self.max_font_size:
            self.current_font_size = self.max_font_size
        self.updateFontSize()
        # Update window size based on new font size
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)


    def resetFontSize(self):
        # Reset font size to default
        self.current_font_size = self.default_font_size
        self.updateFontSize()
        # Update window size based on default font size
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)

    def updateFontSize(self):
        # Update label font size and style
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

    def updateWindowSizeFullscreen(self):
        # Update window size to fullscreen
        screen_rect = QApplication.desktop().screenGeometry()
        self.setGeometry(screen_rect)

    def updateWindowSizeNormal(self):
        # Update window size to normal based on current font size
        font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
        text_width = font_metrics.horizontalAdvance("00:00:00")
        text_height = font_metrics.height()
        self.resize(text_width + 20, text_height + 20)

    def setPresetColors(self, bg_color, fg_color):
        # Set preset background and foreground colors
        self.background_color = bg_color
        self.foreground_color = fg_color
        self.updateFontSize()

    def set_background_color(self):
        # Set custom background color using QColorDialog
        bg_color = QColorDialog.getColor(QColor(self.background_color), self, "Select Background Colour")
        if bg_color.isValid():
            self.background_color = bg_color.name()
            self.updateFontSize()

    def set_foreground_color(self):
        # Set custom foreground color using QColorDialog
        fg_color = QColorDialog.getColor(QColor(self.foreground_color), self, "Select Foreground Colour")
        if fg_color.isValid():
            self.foreground_color = fg_color.name()
            self.updateFontSize()

    def wheelEvent(self, event):
        # Handle mouse wheel event to change font size
        delta = event.angleDelta().y()
        if delta > 0:
            self.changeFontSize(5)
        else:
            self.changeFontSize(-5)

    def mousePressEvent(self, event):
        # Handle mouse press event (middle button to reset font size)
        if event.button() == Qt.MiddleButton:
            self.resetFontSize()

    def mouseDoubleClickEvent(self, event):
        # Handle mouse double-click event (left button to toggle fullscreen)
        if event.button() == Qt.LeftButton:
            self.toggleFullscreen()

    def resizeEvent(self, event):
        # Handle resize event to center the label and keep alignment
        self.label.setGeometry(self.rect())
        self.label.setAlignment(Qt.AlignCenter)
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Clock()
    sys.exit(app.exec_())
