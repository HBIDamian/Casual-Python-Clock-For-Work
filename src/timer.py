import os
import sys
import time
import warnings
import webbrowser

from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QAction, QMessageBox, QMenu
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QFontMetrics, QFontDatabase

from .colour_functions import set_background_color, set_foreground_color, set_preset_colors
from .window_functions import toggle_fullscreen, update_window_size_fullscreen, update_window_size_normal, change_font_size

warnings.filterwarnings("ignore", category=UserWarning)

class Timer(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initial settings
        self.default_font_size = 200
        self.current_font_size = self.default_font_size
        self.min_font_size = 50
        self.max_font_size = 480
        self.is_fullscreen = False
        self.timer_running = False
        self.elapsed_time = 0
        self.pinnedWindow = False
        self.foreground_color = 'white'
        self.background_color = 'black'
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.setWindowTitle('Digital Timer')
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
        # Load custom font (adjust the path as needed)
        font_path = os.path.join(os.path.dirname(__file__), '../Assets/Font/seven-leds.ttf')
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print("Failed to load font")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]

    def resetFontSize(self):
        self.current_font_size = self.default_font_size
        self.updateFontSize()

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

        # Toggle fullscreen action
        fullscreen_action = QAction('Toggle Fullscreen', self)
        fullscreen_action.setShortcut('F')
        fullscreen_action.triggered.connect(self.toggleFullscreen)
        settings_menu.addAction(fullscreen_action)

        # Toggle Start/Stop action
        start_stop_action = QAction('Start/Stop', self)
        start_stop_action.setShortcut('Space')
        start_stop_action.triggered.connect(self.toggleTimer)
        settings_menu.addAction(start_stop_action)

        # Reset timer action
        reset_action = QAction('Reset', self)
        reset_action.setShortcut('R')
        reset_action.triggered.connect(self.resetTimer)
        settings_menu.addAction(reset_action)


        help_menu = self.menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        help_action = QAction('Shortcuts', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def show_about(self):
        about_message = (
            "Idle Digital Timer (using Python)\n\n"
            "A simple digital Timer application\n"
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
            "Space\t Start/Stop Timer\n"
            "R\t Reset Timer\n"
            "-, _\t Decrease Font Size\n"
            "+, =\t Increase Font Size\n"
            "0, F5\t Reset Font Size\n"
            "/, ?, F1 \t Show Help\n"
            "Settings > Colours > Background Colour: Change Background Colour\n"
            "Settings > Colours > Foreground Colour: Change Foreground Colour"
        )
        QMessageBox.information(self, "Help", help_message)

    def togglePinWindow(self):
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

    def toggleTimer(self):
        # Toggle start/stop of the timer
        if self.timer_running:
            self.timer.stop()
        else:
            self.timer.start(1000)  # Update every second
        self.timer_running = not self.timer_running

    def resetTimer(self):
        # Reset timer to 00:00:00 and stop it
        self.elapsed_time = 0
        self.updateTime()
        self.timer.stop()
        self.timer_running = False

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
        if event.key() == Qt.Key_F or event.key() == Qt.Key_F11:
            self.toggleFullscreen()
        elif event.key() == Qt.Key_Space:
            self.toggleTimer()
        elif event.key() == Qt.Key_R:
            self.resetTimer()
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

    def wheelEvent(self, event):
        # Handle mouse wheel event to change font size
        delta = event.angleDelta().y()
        if delta > 0:
            change_font_size(self, 5)
        else:
            change_font_size(self, -5)

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

    def resetFontSize(self):
        self.current_font_size = self.default_font_size
        self.updateFontSize()

    def toggle_menubar(self):
        if self.menubar.isVisible():
            self.menubar.hide()
        else:
            self.menubar.show()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     timer = Timer()
#     sys.exit(app.exec_())
