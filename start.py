import os
import sys
import time
from datetime import datetime
import tkinter as tk
from tkinter import font, Menu, ttk

from PIL import Image, ImageDraw, ImageFont, ImageTk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS # PyInstaller creates this attribute
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SevenSegmentDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seven Segment Display")
        self.root.geometry("340x360")
        self.root.resizable(False, False)
        self.root.configure(bg="#16161d")
        self.root.option_add('*tearOff', False)
        self.root.focus_force()

        # TTK style configuration
        style = ttk.Style(self.root)
        style.theme_use("clam")  # ('aqua', 'clam', 'alt', 'default', 'classic')
        style.configure(
            "My.TButton",
            font=("Courier", 20, "bold"),
            padding=8,
            relief="flat",  # flat, groove, raised, ridge, solid, or sunken
            foreground="#FFFFFF",
            background="#44444a"
        )
        style.map(
            "My.TButton",
            foreground=[("active", "#FFFFFF")],
            background=[("active", "#737377")],
            relief=[("pressed", "groove"), ("active", "sunken")]
        )
        self.main_menu()

    def main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#1E1E1E")

        label = tk.Label(
            self.root,
            text="Choose an Option",
            font=("Courier", 24, "normal"),
            bg="#1E1E1E",
            fg="#FFFFFF",
        )
        label.pack(pady=20)

        buttons = [
            ("Open Clock", self.open_clock),
            ("Open Stopwatch", self.open_stopwatch),
            ("Open Both", self.open_clock_and_stopwatch),
            ("Exit", self.root.quit),
        ]

        for text, command in buttons:
            button = ttk.Button(self.root, text=text, command=command, style="My.TButton")
            button.pack(pady=8, padx=16, fill=tk.X)

        footer = tk.Label(
            self.root,
            text="Made by Damian Hall-Beal",
            font=("Courier", 16, "normal"),
            bg="#1E1E1E",
            fg="#FFFFFF",
        )
        footer.pack(pady=(10, 20), side=tk.BOTTOM, fill=tk.X)

    def open_clock(self):
        self.root.iconify()
        clock_window = ClockWindow(self.root)
        clock_window.window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_window(clock_window)
        )

    def open_stopwatch(self):
        self.root.iconify()
        stopwatch_window = StopwatchWindow(self.root)
        stopwatch_window.window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_window(stopwatch_window)
        )

    def open_clock_and_stopwatch(self):
        self.root.iconify()
        clock_window = ClockWindow(self.root)
        stopwatch_window = StopwatchWindow(self.root)
        clock_window.window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_window(clock_window)
        )
        stopwatch_window.window.protocol(
            "WM_DELETE_WINDOW", lambda: self.close_window(stopwatch_window)
        )

    def close_window(self, window):
        window.window.destroy()
        open_windows = [
            w for w in self.root.winfo_children()
            if isinstance(w, tk.Toplevel) and w.winfo_exists()
        ]
        if open_windows:
            open_windows[0].lift()
            open_windows[0].focus_force()
        else:
            self.root.deiconify()


class CustomFontLabel(tk.Label):
    """
    A label that uses a custom 7-segment font and re-renders on resize.
    """
    def __init__(
        self,
        master,
        text="",
        font_path=None,
        font_size=40,
        color=(255, 255, 255),
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.font_path = font_path or resource_path("assets/7segment.ttf")
        self.font_size = font_size
        self.text = text
        self.color = color
        self.render_text()

    def render_text(self):
        """
        Create a PIL image, draw the text using a custom font, and attach
        it to this Label as a PhotoImage.
        """
        try:
            custom_font = ImageFont.truetype(self.font_path, self.font_size)
        except Exception as e:
            print(f"Error loading font: {e}. Using default font.")
            custom_font = ImageFont.load_default()

        image_width = self.master.winfo_width()
        image_height = self.master.winfo_height()

        if image_width <= 1 or image_height <= 1:
            image_width = 300
            image_height = 100

        image = Image.new("RGB", (image_width, image_height), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        text_bbox = draw.textbbox((0, 0), self.text, font=custom_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        scale_factor = min(
            image_width / (text_width + 20),
            image_height / (text_height + 20)
        )
        new_font_size = int(self.font_size * scale_factor)

        try:
            custom_font = ImageFont.truetype(self.font_path, new_font_size)
        except Exception as e:
            print(f"Error scaling font: {e}. Using default font.")
            custom_font = ImageFont.load_default()

        # Center the text
        x_pos = (image_width - text_width * scale_factor) / 2
        y_pos = (image_height - text_height * scale_factor) / 2

        draw.text((x_pos, y_pos), self.text, font=custom_font, fill=self.color)

        self.photo = ImageTk.PhotoImage(image)
        self.config(image=self.photo)

    def set_text(self, text, color=(255, 255, 255)):
        """
        Update both the label text and color, then re-render.
        """
        self.text = text
        self.color = color
        self.render_text()


class ClockWindow:
    """
    A Toplevel window showing the current time in a 7-segment display.
    """
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title("Clock")
        self.window.geometry("300x100")

        self.label = CustomFontLabel(self.window, font_size=40)
        self.label.pack(expand=True, fill=tk.BOTH)

        self.is_pinned = tk.BooleanVar(value=False)

        self.clock_menubar = Menu(self.window)
        self.create_menu()
        self.window.config(menu=self.clock_menubar)
        self.window.bind("<FocusIn>", self.on_focus_in)

        # === DRAG-ANYWHERE SETUP ===
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.window.bind("<ButtonPress-1>", self.on_drag_start)
        self.window.bind("<B1-Motion>", self.on_drag_move)
        self.window.bind("<F1>", self.on_help_shortcut)

        # Local key bindings
        self.window.bind("<p>", self.toggle_pin_keyboard)
        self.window.bind("<slash>", self.on_help_shortcut)
        self.window.bind("?", self.on_help_shortcut)

        self.update_time()
        self.window.bind("<Configure>", self.on_resize)

    def create_menu(self):
        clock_menu = Menu(self.clock_menubar, tearoff=0)
        clock_menu.add_checkbutton(
            label="Toggle Pin Window (P)",
            variable=self.is_pinned,
            command=self.toggle_pin_checkbutton
        )
        self.clock_menubar.add_cascade(label="Settings", menu=clock_menu)

        help_menu = Menu(self.clock_menubar, tearoff=0)
        help_menu.add_command(
            label="Instructions",
            command=lambda: self.show_help(
                "Clock Help",
                "Instructions:\n\n"
                "  - Toggle pin: Use the menu or press 'P'.\n"
                "  - Drag anywhere in the window to move it."
            ),
        )
        self.clock_menubar.add_cascade(label="Help", menu=help_menu)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.label.set_text(current_time)
        self.window.after(500, self.update_time)

    def on_resize(self, event=None):
        self.label.render_text()

    def on_drag_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_move(self, event):
        x = self.window.winfo_x() + (event.x - self.drag_start_x)
        y = self.window.winfo_y() + (event.y - self.drag_start_y)
        self.window.geometry(f"+{x}+{y}")

    def on_focus_in(self, event=None):
        self.root.config(menu=self.clock_menubar)

    def toggle_pin_checkbutton(self):
        pinned = self.is_pinned.get()
        self.window.attributes("-topmost", pinned)
        self.update_window_title()

    def toggle_pin_keyboard(self, event=None):
        pinned = not self.is_pinned.get()
        self.is_pinned.set(pinned)
        self.window.attributes("-topmost", pinned)
        self.update_window_title()

    def update_window_title(self):
        if self.is_pinned.get():
            self.window.title("Clock - 📌")
        else:
            self.window.title("Clock")

    def on_help_shortcut(self, event=None):
        self.show_help(
            "Clock Help",
            "Instructions:\n\n"
            "  - Toggle pin: Press 'P' or use the menu.\n"
            "  - Drag anywhere in the window to move it."
        )

    def show_help(self, title, message):
        help_window = tk.Toplevel(self.window)
        help_window.title(title)
        label = tk.Label(help_window, text=message, justify=tk.LEFT, padx=10, pady=10)
        label.pack(expand=True, fill=tk.BOTH)


class StopwatchWindow:
    """
    A Toplevel window functioning as a stopwatch with Start/Stop/Reset capabilities.
    """
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.title("Stopwatch")
        self.window.geometry("300x100")

        self.running = False
        self.start_time = None
        self.elapsed_time = 0

        self.label = CustomFontLabel(self.window, text="00:00:00", font_size=40)
        self.label.pack(expand=True, fill=tk.BOTH)

        self.is_pinned = tk.BooleanVar(value=False)

        self.stopwatch_menubar = Menu(self.window)
        self.create_menu()
        self.window.config(menu=self.stopwatch_menubar)
        self.window.bind("<FocusIn>", self.on_focus_in)

        # Control buttons frame
        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack()

        self.start_button = tk.Button(self.control_frame, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=2, padx=5)

        # === DRAG-ANYWHERE SETUP ===
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.window.bind("<ButtonPress-1>", self.on_drag_start)
        self.window.bind("<B1-Motion>", self.on_drag_move)

        # Local key bindings
        self.window.bind("<space>", self.toggle_start_stop)
        self.window.bind("<r>", lambda e: self.reset())
        self.window.bind("<p>", self.toggle_pin_keyboard)
        self.window.bind("<slash>", self.on_help_shortcut)
        self.window.bind("?", self.on_help_shortcut)

        self.window.bind("<Configure>", self.on_resize)

    def create_menu(self):
        stopwatch_menu = Menu(self.stopwatch_menubar, tearoff=0)
        stopwatch_menu.add_checkbutton(
            label="Toggle Pin Window (P)",
            variable=self.is_pinned,
            command=self.toggle_pin_checkbutton
        )
        stopwatch_menu.add_command(
            label="Start/Stop Stopwatch (Spacebar)",
            command=self.toggle_start_stop
        )
        stopwatch_menu.add_command(
            label="Reset Stopwatch (R)",
            command=self.reset
        )
        self.stopwatch_menubar.add_cascade(label="Settings", menu=stopwatch_menu)

        help_menu = Menu(self.stopwatch_menubar, tearoff=0)
        help_menu.add_command(
            label="Instructions",
            command=lambda: self.show_help(
                "Stopwatch Help",
                "Instructions:\n\n"
                "  - Start/Stop: Press 'Spacebar' or use the Start/Stop button.\n"
                "  - Reset: Press 'R' or use the Reset button.\n"
                "  - Toggle pin: Press 'P' or use the menu.\n"
                "  - Drag anywhere in the window to move it."
            ),
        )
        self.stopwatch_menubar.add_cascade(label="Help", menu=help_menu)

    def on_focus_in(self, event=None):
        self.root.config(menu=self.stopwatch_menubar)

    def toggle_pin_checkbutton(self):
        pinned = self.is_pinned.get()
        self.window.attributes("-topmost", pinned)
        self.update_window_title()

    def toggle_pin_keyboard(self, event=None):
        pinned = not self.is_pinned.get()
        self.is_pinned.set(pinned)
        self.window.attributes("-topmost", pinned)
        self.update_window_title()

    def update_window_title(self):
        if self.is_pinned.get():
            self.window.title("Stopwatch - 📌")
        else:
            self.window.title("Stopwatch")

    def on_drag_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_move(self, event):
        x = self.window.winfo_x() + (event.x - self.drag_start_x)
        y = self.window.winfo_y() + (event.y - self.drag_start_y)
        self.window.geometry(f"+{x}+{y}")

    def toggle_start_stop(self, event=None):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.label.set_text(self.label.text, color=(0, 255, 0))
            self.update_stopwatch()

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            self.label.set_text(self.label.text, color=(255, 0, 0))

    def reset(self):
        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.label.set_text("00:00:00", color=(255, 255, 255))

    def update_stopwatch(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(self.elapsed_time), 60)
            hours, minutes = divmod(minutes, 60)
            self.label.set_text(
                f"{hours:02}:{minutes:02}:{seconds:02}",
                color=(0, 255, 0)
            )
            self.window.after(100, self.update_stopwatch)

    def on_help_shortcut(self, event=None):
        self.show_help(
            "Stopwatch Help",
            "Instructions:\n\n"
            "  - Start/Stop: Press 'Spacebar' or use the Start/Stop button.\n"
            "  - Reset: Press 'R' or use the Reset button.\n"
            "  - Toggle pin: Press 'P' or use the menu.\n"
            "  - Drag anywhere in the window to move it."
        )

    def show_help(self, title, message):
        help_window = tk.Toplevel(self.window)
        help_window.title(title)
        label = tk.Label(help_window, text=message, justify=tk.LEFT, padx=10, pady=10)
        label.pack(expand=True, fill=tk.BOTH)

    def on_resize(self, event=None):
        self.label.render_text()


if __name__ == "__main__":
    root = tk.Tk()
    app = SevenSegmentDisplayApp(root)
    root.mainloop()
