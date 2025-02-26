import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from typing import Protocol

TITLE = "TPU Tester"


class Presenter(Protocol):
    def handle_start_test(self, event=None) -> None: ...


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)

        # Control buttons
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)
        # Log display
        self.log_widget = scrolledtext.ScrolledText(self, state="normal", height=5)
        self.log_widget.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    def init_ui(self, presenter: Presenter):
        self.start_button = tk.Button(
            self.control_frame, text="Start", command=presenter.handle_start_test
        )
        self.start_button.pack(pady=5)

    def get_tpu_barcode(self) -> str:
        return simpledialog.askstring(
            title="TPU Barcode",
            prompt="Scan TPU QR Code or \n\r "
            "type the code with format XXXXXXX-XXXXX",
        )

    def verify_output_leds(self) -> bool:
        return messagebox.askyesno("TPU Output Leds", "Are Leds o1,o2,o3,o4 on?")

    def update_result(self, text, color):
        self.result_label.config(text=text, bg=color)

    def update_log(self, message):
        self.log_widget.configure(state="normal")
        self.log_widget.insert(tk.END, message + "\n")
        self.log_widget.see(tk.END)  # Scroll to the bottom
        self.log_widget.configure(state="disabled")
        self.log_widget.update()  # Refresh the widget
