from curses import wrapper
from pathlib import Path
from .cli import menu
import tkinter as tk
from tkinter import filedialog

def rename():
    choices = ['Enter directory path','Open file explorer','Exit']
    selected = wrapper(menu,choices)
    if choices[selected] == 'Enter directory path':
        directory = Path(input('Enter the selected directory: '))
        rename_sort(directory)
    elif choices[selected] == 'Open file explorer':
        root = tk.Tk()
        root.withdraw()
        directory = Path(filedialog.askdirectory(title='Select the chosen directory: '))
        rename_sort(directory)
    else:
        return

def rename_sort(directory):
    if not directory.is_dir():
        print("Invalid directory")
        return
    files = sorted(
            f for f in directory.iterdir()
            if f.is_file()
            )
    for count,file in enumerate(files,start=1):
        file.rename(directory/f"ep{count}-")        
