from tkinter import *
from random import randint
import os
import sys


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def key_press(event):
	global key_pressed
	if not key_pressed:
		key_pressed = True
		# event.char

def key_release(event):
	global key_pressed
	key_pressed = False

def main():
	global key_pressed
	
	key_pressed = False
	
	root = Tk()
	root.geometry(f'500x500+{root.winfo_screenwidth() // 2 - 250}+{root.winfo_screenheight() // 2 - 250}')
	root.resizable(False, False)
	root.title('NumGuessr')
	root.iconbitmap(resource_path("icon.ico"))

	root.bind(f"<KeyPress>", lambda event: key_press(event))
	root.bind(f"<KeyRelease>", lambda event: key_release(event)) 

	title = Label(text="naslov")
	title.place(x=50, y=50, width=100, height=100)

	root.mainloop()


if __name__ == '__main__':
	main()
