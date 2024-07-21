import os
import time
import warnings
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QLabel, QAction, QMessageBox, QMenu
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontDatabase, QFontMetrics
from .colour_functions import set_background_color, set_foreground_color, set_preset_colors
from .window_functions import toggle_fullscreen, update_window_size_fullscreen, update_window_size_normal, change_font_size

warnings.filterwarnings("ignore", category=UserWarning)

class Clock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.default_font_size = 200
        self.current_font_size = self.default_font_size
        self.min_font_size = 50
        self.max_font_size = 480
        self.is_fullscreen = False
        self.pinnedWindow = False
        self.foreground_color = 'white'
        self.background_color = 'black'
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.setWindowTitle('Digital Clock')
        self.initUI()

    def initUI(self):
        self.loadCustomFont()
        self.createLabel()
        self.createTimer()
        self.setInitialWindowSize()
        self.createMenuBar()
        self.show()

    def loadCustomFont(self):
        font_path = os.path.join(os.path.dirname(__file__), '../Assets/Font/seven-leds.ttf')
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print("Failed to load font")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    def createLabel(self):
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(self.geometry())
        self.setCentralWidget(self.label)
        self.updateFontSize()
        self.updateTime()

    def createTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(250)

    def setInitialWindowSize(self):
        if not self.is_fullscreen:
            font_metrics = QFontMetrics(QFont(self.font_family, self.current_font_size))
            text_width = font_metrics.horizontalAdvance("00:00:00")
            text_height = font_metrics.height()
            self.resize(text_width + 20, text_height + 20)

    def createMenuBar(self):
        self.menubar = self.menuBar()
        settings_menu = self.menubar.addMenu('Settings')

        pin_action = QAction('Pin Window', self)
        pin_action.setCheckable(True)
        pin_action.triggered.connect(self.togglePinWindow)
        settings_menu.addAction(pin_action)
        settings_menu.addSeparator()

        colours_menu = QMenu('Colours', self)
        bg_color_action = QAction('Background Colour', self)
        bg_color_action.triggered.connect(lambda: set_background_color(self))
        colours_menu.addAction(bg_color_action)
        fg_color_action = QAction('Foreground Colour', self)
        fg_color_action.triggered.connect(lambda: set_foreground_color(self))
        colours_menu.addAction(fg_color_action)
        colours_menu.addSeparator()

        colours_menu.addAction('Swap Colours').triggered.connect(lambda: set_preset_colors(self, self.foreground_color, self.background_color))
        colours_menu.addAction('Random').triggered.connect(lambda: set_preset_colors(self, '#' + os.urandom(6).hex(), '#' + os.urandom(6).hex()))
        colours_menu.addSeparator()
        settings_menu.addMenu(colours_menu)

        presets_menu = QMenu('Presets', self)
        presets_menu.addSeparator()

        presets_dark_menu = QMenu('Dark Themes', self)
        presets_light_menu = QMenu('Light Themes', self)
        presets_custom_menu = QMenu('Custom Themes', self)

        presets_dark_menu.addAction('Dark Mode').triggered.connect(lambda: set_preset_colors(self, '#121212', '#f0f0f0'))
        presets_dark_menu.addAction('White on Black').triggered.connect(lambda: set_preset_colors(self, 'black', 'white'))
        presets_dark_menu.addAction('Red on Black').triggered.connect(lambda: set_preset_colors(self, 'black', 'red'))
        presets_dark_menu.addAction('Dark Green on Black').triggered.connect(lambda: set_preset_colors(self, 'black', 'green'))
        presets_dark_menu.addAction('Dark Blue on Black').triggered.connect(lambda: set_preset_colors(self, 'black', 'blue'))

        presets_light_menu.addAction('Light Mode').triggered.connect(lambda: set_preset_colors(self, '#f0f0f0', '#121212'))
        presets_light_menu.addAction('Black on White').triggered.connect(lambda: set_preset_colors(self, 'white', 'black'))
        presets_light_menu.addAction('White on Red').triggered.connect(lambda: set_preset_colors(self, 'red', 'white'))

        presets_custom_menu.addAction('Sky Blue').triggered.connect(lambda: set_preset_colors(self, '#55aaff', '#aaffff'))
        presets_custom_menu.addAction('Blazing Orange & Mahogany').triggered.connect(lambda: set_preset_colors(self, '#730000', '#FF4D00'))
        presets_custom_menu.addAction('Royal Purple & Periwinkle').triggered.connect(lambda: set_preset_colors(self, '#7093FF', '#330066'))

        presets_menu.addMenu(presets_light_menu)
        presets_menu.addMenu(presets_dark_menu)
        presets_menu.addMenu(presets_custom_menu)

        colours_menu.addMenu(presets_menu)

        help_menu = self.menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        help_action = QAction('Shortcuts', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def togglePinWindow(self):
        self.pinnedWindow = not self.pinnedWindow
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self.pinnedWindow)
        self.show()

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

    def open_github(self):
        webbrowser.open("https://github.com/HBIDamian/Casual-Python-Clock-For-Work")

    def show_help(self):
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
        self.label.setText(time.strftime("%H:%M:%S"))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F or event.key() == Qt.Key_F11:
            toggle_fullscreen(self)
        elif event.key() == Qt.Key_P:
            self.togglePinWindow()
        elif event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            change_font_size(self, 5)
        elif event.key() in (Qt.Key_Minus, Qt.Key_Underscore):
            change_font_size(self, -5)
        elif event.key() in (Qt.Key_0, Qt.Key_F5):
            self.resetFontSize()
        elif event.key() == Qt.Key_T or event.key() == Qt.Key_M:
            self.toggle_menubar()
        elif event.key() in (Qt.Key_Slash, Qt.Key_Question, Qt.Key_F1):
            self.show_help()

    def updateFontSize(self):
        self.label.setStyleSheet(
            f"font-family: '{self.font_family}'; "
            f"font-size: {self.current_font_size}px; "
            f"letter-spacing: .2em; "
            f"color: {self.foreground_color}; "
            f"background-color: {self.background_color};"
        )
        if not self.is_fullscreen:
            update_window_size_normal(self)

    def resizeEvent(self, event):
        self.label.setGeometry(self.rect())
        self.label.setAlignment(Qt.AlignCenter)
        super().resizeEvent(event)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            change_font_size(self, 5)
        else:
            change_font_size(self, -5)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.resetFontSize()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            toggle_fullscreen(self)

    def resetFontSize(self):
        self.current_font_size = self.default_font_size
        self.updateFontSize()

    def toggle_menubar(self):
        if self.menubar.isVisible():
            self.menubar.hide()
        else:
            self.menubar.show()
