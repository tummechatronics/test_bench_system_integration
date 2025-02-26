import logging
import tkinter as tk


class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.widget = widget
        self.widget.configure(state="disabled")
        self.widget.tag_config("INFO", foreground="black")
        self.widget.tag_config("PASS", foreground="green")
        self.widget.tag_config("FAIL", foreground="red")
        self.widget.tag_config("DEBUG", foreground="grey")
        self.widget.tag_config("WARNING", foreground="orange")
        self.widget.tag_config("CRITICAL", foreground="red", underline=1)

    def emit(self, record):
        self.widget.configure(state="normal")
        # Append message (record) to the widget
        msg = (
            self.format(record)
            if isinstance(record, logging.LogRecord)
            else str(record)
        )
        self.widget.insert(tk.END, msg + "\n")
        self.widget.see(tk.END)  # Scroll to the bottom
        self.widget.configure(state="disabled")
        self.widget.update()
