import json
import os
import webbrowser
import warnings

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontMetrics, QFontDatabase
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QAction, QMessageBox, QMenu
)

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

# Ignore UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)

class Stopwatch(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initial settings
        self.default_font_size = 200
        self.current_font_size = self.default_font_size
        self.min_font_size = 50
        self.max_font_size = 480
        self.is_fullscreen = False
        self.stopwatch_running = False
        self.elapsed_time = 0
        self.pinnedWindow = False
        self.foreground_color = 'white'
        self.background_color = 'black'
        self.setWindowTitle('Digital Stopwatch')
        self.setWindowIconText('Digital Stopwatch')
        self.initUI()

    def initUI(self):
        # Initialize UI components
        self.loadCustomFont()
        self.createLabel()
        self.createStopwatch()
        self.setInitialWindowSize()
        self.loadThemes()
        self.createMenuBar()
        self.show()

    def loadCustomFont(self):
        # Load custom font
        font_path = os.path.join(os.path.dirname(__file__), '../Assets/Font/seven-leds.ttf')
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print("Failed to load font")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    def createLabel(self):
        # Create main label for displaying time
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.updateFontSize()
        self.updateTime()

    def createStopwatch(self):
        # Create stopwatch to update time display
        self.stopwatch = QTimer(self)
        self.stopwatch.timeout.connect(self.updateTime)

    def setInitialWindowSize(self):
        # Set initial window size based on font metrics
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)

    def loadThemes(self):
        # Load theme configurations from file
        themes_path = os.path.join(os.path.dirname(__file__), '../config/themes.json')
        with open(themes_path, 'r') as file:
            self.themes = json.load(file)

    def createMenuBar(self):
        # Create menu bar with actions and menus
        self.menubar = self.menuBar()
        settings_menu = self.menubar.addMenu('Stopwatch Settings')

        # Pin Window Action
        pin_action = QAction('Pin Window', self)
        pin_action.setCheckable(True)
        pin_action.triggered.connect(self.togglePinWindow)
        settings_menu.addAction(pin_action)

        # Toggle Fullscreen Action
        fullscreen_action = QAction('Toggle Fullscreen', self)
        fullscreen_action.setShortcut('F')
        fullscreen_action.triggered.connect(self.toggleFullscreen)
        settings_menu.addAction(fullscreen_action)

        settings_menu.addSeparator()

        # Start/Stop Stopwatch Action
        start_stop_action = QAction('Start/Stop', self)
        start_stop_action.setShortcut('Space')
        start_stop_action.triggered.connect(self.toggleStopwatch)
        settings_menu.addAction(start_stop_action)

        # Reset Stopwatch Action
        reset_action = QAction('Reset', self)
        reset_action.setShortcut('R')
        reset_action.triggered.connect(self.resetStopwatch)
        settings_menu.addAction(reset_action)

        settings_menu.addSeparator()

        # Colours Menu
        colours_menu = QMenu('Colours', self)
        self.addColourActions(colours_menu)
        settings_menu.addMenu(colours_menu)

        # Presets Menu
        presets_menu = QMenu('Presets', self)
        self.populateThemesMenu(presets_menu, 'Light Themes')
        self.populateThemesMenu(presets_menu, 'Dark Themes')
        self.populateThemesMenu(presets_menu, 'Custom Themes')
        colours_menu.addMenu(presets_menu)

        # Help Menu
        help_menu = self.menubar.addMenu('Help')
        self.addHelpActions(help_menu)

    def addColourActions(self, menu):
        # Add colour-related actions to the menu
        bg_color_action = QAction('Background Colour', self)
        bg_color_action.triggered.connect(lambda: set_background_color(self))
        menu.addAction(bg_color_action)

        fg_color_action = QAction('Foreground Colour', self)
        fg_color_action.triggered.connect(lambda: set_foreground_color(self))
        menu.addAction(fg_color_action)

        menu.addSeparator()

        swap_colours_action = QAction('Swap Colours', self)
        swap_colours_action.triggered.connect(lambda: set_preset_colors(self, self.foreground_color, self.background_color))
        menu.addAction(swap_colours_action)

        random_colours_action = QAction('Random', self)
        random_colours_action.triggered.connect(lambda: set_preset_colors(self, '#' + os.urandom(6).hex(), '#' + os.urandom(6).hex()))
        menu.addAction(random_colours_action)

        menu.addSeparator()

    def addHelpActions(self, menu):
        # Add help-related actions to the menu
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)

        help_action = QAction('Shortcuts', self)
        help_action.triggered.connect(self.show_help)
        menu.addAction(help_action)

    def show_about(self):
        # Show the 'About' message box
        about_message = (
            "Idle Digital Stopwatch (using Python)\n\n"
            "A simple digital Stopwatch application\n"
            "Created by HBIDamian"
        )
        about_message_box = QMessageBox()
        about_message_box.setWindowTitle("About")
        about_message_box.setText(about_message)
        about_message_box.setInformativeText("For more information, visit the GitHub repository.")
        about_message_box.setIcon(QMessageBox.Information)

        github_button = about_message_box.addButton("GitHub", QMessageBox.ActionRole)
        github_button.clicked.connect(self.open_github)

        shortcuts_button = about_message_box.addButton("Shortcuts", QMessageBox.ActionRole)
        shortcuts_button.clicked.connect(self.show_help)

        about_message_box.exec_()

    def open_github(self):
        # Open the GitHub repository in the web browser
        webbrowser.open("https://github.com/HBIDamian/Casual-Python-Clock-For-Work")

    def show_help(self):
        # Show the help message box
        help_message = (
            "Keyboard Shortcuts:\n\n"
            "F, F11\t Toggle Fullscreen\n"
            "M, T\t Toggle Menubar\n"
            "P\t Pin Window\n"
            "Space\t Start/Stop Stopwatch\n"
            "R\t Reset Stopwatch\n"
            "-, _\t Decrease Font Size\n"
            "+, =\t Increase Font Size\n"
            "0, F5\t Reset Font Size\n"
            "/, ?, F1 \t Show Help\n"
            "Settings > Colours > Background Colour: Change Background Colour\n"
            "Settings > Colours > Foreground Colour: Change Foreground Colour"
        )
        QMessageBox.information(self, "Help", help_message)

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
        # Toggle the pin state of the window
        self.pinnedWindow = not self.pinnedWindow
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.pinnedWindow)
        self.show()

    def toggleFullscreen(self):
        # Toggle fullscreen mode
        if self.is_fullscreen:
            self.showNormal()
            self.updateWindowSizeNormal()
        else:
            self.showFullScreen()
            self.updateWindowSizeFullscreen()
        self.is_fullscreen = not self.is_fullscreen

    def toggleStopwatch(self):
        # Toggle start/stop of the stopwatch
        if self.stopwatch_running:
            self.stopwatch.stop()
        else:
            self.stopwatch.start(1000)  # Update every second
        self.stopwatch_running = not self.stopwatch_running

    def resetStopwatch(self):
        # Reset stopwatch to 00:00:00 and stop it
        self.elapsed_time = 0
        self.updateTime()
        self.stopwatch.stop()
        self.stopwatch_running = False

    def updateTime(self):
        # Update time displayed on the label
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.elapsed_time += 1

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

    def keyPressEvent(self, event):
        # Handle key press events
        key = event.key()
        if key in [Qt.Key_F, Qt.Key_F11]:
            self.toggleFullscreen()
        elif key == Qt.Key_Space:
            self.toggleStopwatch()
        elif key == Qt.Key_R:
            self.resetStopwatch()
        elif key in [Qt.Key_Plus, Qt.Key_Equal]:
            change_font_size(self, 5)
        elif key in [Qt.Key_Minus, Qt.Key_Underscore]:
            change_font_size(self, -5)
        elif key in [Qt.Key_P]:
            self.togglePinWindow()
        elif key in [Qt.Key_0, Qt.Key_F5]:
            self.resetFontSize()
        elif key in [Qt.Key_T, Qt.Key_M]:
            self.toggle_menubar()
        elif key in [Qt.Key_Slash, Qt.Key_Question, Qt.Key_F1]:
            self.show_help()

    def wheelEvent(self, event):
        # Handle mouse wheel event to change font size
        delta = event.angleDelta().y()
        change_font_size(self, 5 if delta > 0 else -5)

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

    def toggle_menubar(self):
        # Toggle visibility of the menu bar
        if self.menubar.isVisible():
            self.menubar.hide()
        else:
            self.menubar.show()
