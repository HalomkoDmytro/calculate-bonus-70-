import locale
import logging
import os
import sys
import tkinter as tk
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from tkcalendar import DateEntry

from LoggerWriter import LoggerWriter
from service.CalculateService import process

Path("log").mkdir(parents=True, exist_ok=True)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('log/error.log', when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
logger.addHandler(handler)
sys.stdout = LoggerWriter(logging.debug)
sys.stderr = LoggerWriter(logging.warning)


class Bonus70App:
    def __init__(self, root):
        self.root = root
        root.geometry("500x250")
        self.root.title("Розрахунок премії 70 000 грн по БЗ+")

        locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')

        self.label1 = tk.Label(root, text="Початок періода:")
        self.label1.pack(pady=5)
        self.cal1 = DateEntry(root, width=12, background='darkblue',
                              foreground='white', borderwidth=2, locale='uk_UA')
        self.cal1.pack(pady=5)

        self.label2 = tk.Label(root, text="Кінець періода:")
        self.label2.pack(pady=5)
        self.cal2 = DateEntry(root, width=12, background='darkblue',
                              foreground='white', borderwidth=2, locale='uk_UA')
        self.cal2.pack(pady=5)

        self.button = tk.Button(root, text="СТАРТ", command=self.start_progress)
        self.button.pack(pady=20)

        self.destination_folder_btn = tk.Button(root, text="Відкрити папку Destination", command=self.open_folder,
                                                bg='lightblue')
        self.destination_folder_btn.pack(pady=10)

        # self.progress_bar = ttk.Progressbar(root, mode='indeterminate')
        # self.progress_bar.pack(pady=10, padx=10, fill=tk.X)

    def start_progress(self):
        # self.progress_bar.start()
        process(self.cal1.get_date(), self.cal2.get_date(), self.root)

    def open_folder(self, folder_path="destination"):
        if folder_path:
            os.startfile(folder_path)


def main():
    root = tk.Tk()
    app = Bonus70App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
