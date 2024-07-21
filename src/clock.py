import json
import os
import time
import warnings
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMessageBox, QMenu
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QFontMetrics
from .colour_functions import (
    set_background_color,
    set_foreground_color,
    set_preset_colors
)
from .window_functions import (
    toggle_fullscreen,
    update_window_size_fullscreen,
    update_window_size_normal,
    change_font_size
)

warnings.filterwarnings("ignore", category=UserWarning)  # Ignore user warnings

class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        # Default settings
        self.default_font_size = 200
        self.current_font_size = self.default_font_size
        self.min_font_size = 50
        self.max_font_size = 480
        self.is_fullscreen = False
        self.pinnedWindow = False
        self.foreground_color = 'white'
        self.background_color = 'black'
        self.setWindowTitle('Digital Clock')
        self.initUI()

    def initUI(self):
        # Initialize the user interface
        self.loadCustomFont()
        self.createLabel()
        self.createTimer()
        self.setInitialWindowSize()
        self.loadThemes()
        self.createMenuBar()
        self.show()

    def loadCustomFont(self):
        # Load and set a custom font
        font_path = os.path.join(os.path.dirname(__file__), '../Assets/Font/seven-leds.ttf')
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print("Failed to load font")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    def createLabel(self):
        # Create and configure the time display label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(self.geometry())
        self.setCentralWidget(self.label)
        self.updateFontSize()
        self.updateTime()

    def createTimer(self):
        # Create a timer to update the time every 250 milliseconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(250)

    def setInitialWindowSize(self):
        # Set initial window size based on font size
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)

    def loadThemes(self):
        # Load themes from configuration file
        themes_path = os.path.join(os.path.dirname(__file__), '../config/themes.json')
        with open(themes_path, 'r') as file:
            self.themes = json.load(file)

    def createMenuBar(self):
        # Create and configure the menu bar
        self.menubar = self.menuBar()
        settings_menu = self.menubar.addMenu('Clock Settings')

        # Pin Window Action
        pin_action = QAction('Pin Window', self)
        pin_action.setCheckable(True)
        pin_action.triggered.connect(self.togglePinWindow)
        settings_menu.addAction(pin_action)

        # Fullscreen Action
        fullscreen_action = QAction('Fullscreen', self)
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(lambda: toggle_fullscreen(self))
        settings_menu.addAction(fullscreen_action)

        settings_menu.addSeparator()

        # Colours Menu
        colours_menu = QMenu('Colours', self)
        bg_color_action = QAction('Background Colour', self)
        bg_color_action.triggered.connect(lambda: set_background_color(self))
        colours_menu.addAction(bg_color_action)

        fg_color_action = QAction('Foreground Colour', self)
        fg_color_action.triggered.connect(lambda: set_foreground_color(self))
        colours_menu.addAction(fg_color_action)

        colours_menu.addSeparator()
        colours_menu.addAction('Swap Colours').triggered.connect(
            lambda: set_preset_colors(self, self.foreground_color, self.background_color)
        )
        colours_menu.addAction('Random').triggered.connect(
            lambda: set_preset_colors(self, '#' + os.urandom(6).hex(), '#' + os.urandom(6).hex())
        )
        colours_menu.addSeparator()
        settings_menu.addMenu(colours_menu)

        # Presets Menu
        presets_menu = QMenu('Presets', self)
        presets_menu.addSeparator()
        self.populateThemesMenu(presets_menu, 'Light Themes')
        self.populateThemesMenu(presets_menu, 'Dark Themes')
        self.populateThemesMenu(presets_menu, 'Custom Themes')
        colours_menu.addMenu(presets_menu)

        # Help Menu
        help_menu = self.menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        help_action = QAction('Shortcuts', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def populateThemesMenu(self, parent_menu, theme_category):
        # Populate the themes menu with theme actions
        themes_menu = QMenu(theme_category, self)
        for theme in self.themes.get(theme_category, []):
            action = QAction(theme['name'], self)
            action.triggered.connect(
                lambda checked, bg=theme['background_color'], fg=theme['foreground_color']: 
                set_preset_colors(self, bg, fg)
            )
            themes_menu.addAction(action)
        parent_menu.addMenu(themes_menu)

    def togglePinWindow(self):
        # Toggle pinning the window on top
        self.pinnedWindow = not self.pinnedWindow
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.pinnedWindow)
        self.show()

    def show_about(self):
        # Show the About dialog
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
        # Open the GitHub repository in the browser
        webbrowser.open("https://github.com/HBIDamian/Casual-Python-Clock-For-Work")

    def show_help(self):
        # Show the help dialog with keyboard shortcuts
        help_message = (
            "Keyboard Shortcuts:\n\n"
            "F, F11\t Toggle Fullscreen\n"
            "M, T\t Toggle Menubar\n"
            "P\t Pin Window\n"
            "-, _\t Decrease Font Size\n"
            "+, =\t Increase Font Size\n"
            "0, F5\t Reset Font Size\n"
            "/, ?, F1 \t Show Help\n"
            "Settings > Colours > Background Colour: Change Background Colour\n"
            "Settings > Colours > Foreground Colour: Change Foreground Colour"
        )
        QMessageBox.information(self, "Help", help_message)

    def updateTime(self):
        # Update the label with the current time
        self.label.setText(time.strftime("%H:%M:%S"))

    def keyPressEvent(self, event):
        # Handle keyboard shortcuts
        if event.key() in (Qt.Key_F, Qt.Key_F11):
            toggle_fullscreen(self)
        elif event.key() == Qt.Key_P:
            self.togglePinWindow()
        elif event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            change_font_size(self, 5)
        elif event.key() in (Qt.Key_Minus, Qt.Key_Underscore):
            change_font_size(self, -5)
        elif event.key() in (Qt.Key_0, Qt.Key_F5):
            self.resetFontSize()
        elif event.key() in (Qt.Key_T, Qt.Key_M):
            self.toggle_menubar()
        elif event.key() in (Qt.Key_Slash, Qt.Key_Question, Qt.Key_F1):
            self.show_help()

    def updateFontSize(self):
        # Update the font size and apply stylesheet
        self.label.setStyleSheet(
            f"font-family: '{self.font_family}'; "
            f"font-size: {self.current_font_size}px; "
            f"letter-spacing: .2em; "
            f"color: {self.foreground_color}; "
            f"background-color: {self.background_color};"
        )
        if not self.is_fullscreen:
            update_window_size_normal(self)

    def resetFontSize(self):
        # Reset font size to default
        self.current_font_size = self.default_font_size
        self.updateFontSize()

    def resizeEvent(self, event):
        # Adjust label size when the window is resized
        self.label.setGeometry(self.rect())
        self.label.setAlignment(Qt.AlignCenter)
        super().resizeEvent(event)

    def wheelEvent(self, event):
        # Adjust font size with mouse wheel
        delta = event.angleDelta().y()
        change_font_size(self, 5 if delta > 0 else -5)

    def toggle_menubar(self):
        # Toggle visibility of the menu bar
        if self.menubar.isVisible():
            self.menubar.hide()
        else:
            self.menubar.show()
