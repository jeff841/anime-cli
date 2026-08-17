from curses import wrapper
from pathlib import Path
from .cli import menu
import tkinter as tk
from tkinter import filedialog
from .constants import EXPLORER_DIR,INV_DIR

def rename():
    choices = ['Enter directory path','Open file explorer','Exit']
    result = wrapper(menu,choices)
    if result.command == 'quit' or result.selected is None:
        return
    if choices[result.selected] == 'Enter directory path':
        directory = Path(input('Enter the selected directory: '))
        rename_sort(directory)
    elif choices[result.selected] == 'Open file explorer':
        root = tk.Tk()
        root.withdraw()
        directory = Path(filedialog.askdirectory(title=EXPLORER_DIR))
        rename_sort(directory)
    else:
        return

def rename_sort(directory):
    if not directory.is_dir():
        print(INV_DIR)
        return
    files = sorted(
            f for f in directory.iterdir()
            if f.is_file()
            )
    for count,file in enumerate(files,start=1):
        file.rename(directory/f"ep{count}-")        
