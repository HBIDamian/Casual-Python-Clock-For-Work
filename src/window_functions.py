from PyQt5.QtGui import QFont, QFontMetrics

def toggle_fullscreen(clock):
    if clock.is_fullscreen:
        clock.showNormal()
        clock.is_fullscreen = False
        update_window_size_normal(clock)
    else:
        clock.showFullScreen()
        clock.is_fullscreen = True
        update_window_size_fullscreen(clock)

def update_window_size_normal(clock):
    font_metrics = QFontMetrics(QFont(clock.font_family, clock.current_font_size))
    text_width = font_metrics.horizontalAdvance("00:00:00")
    text_height = font_metrics.height()
    clock.resize(text_width + 20, text_height + 20)

def update_window_size_fullscreen(clock):
    screen = clock.screen().geometry()
    clock.setGeometry(screen)

def change_font_size(clock, change):
    new_size = clock.current_font_size + change
    if clock.min_font_size <= new_size <= clock.max_font_size:
        clock.current_font_size = new_size
        clock.updateFontSize()
