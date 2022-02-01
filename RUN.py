from tkinter import *
from tkinter import ttk
from threading import Thread
import os

def window_deleted():
    os.system('taskkill /im cmd.exe')

os.system('python discord_bot.py')
os.system('taskkill /im cmd.exe')
root = Tk()
console = Text(width= 85,height = 30)
console.grid()
button = Button(text='Тест')
button.grid(row = 0, column = 1)
root.geometry('700x700')
root.mainloop()
root.protocol('WM_DELETE_WINDOW', window_deleted)
