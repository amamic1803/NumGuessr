from tkinter import *
from random import randint

# resource path funct
def key_press(event):
	global key_pressed
	key_pressed = True
	
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
	root.title('') # dopisati ime
	root.iconbitmap('') # dodati ikonu
	
	root.bind(f"<KeyPress>", lambda event: key_press(event))
	root.bind(f"<KeyRelease>", lambda event: key_release(event)) 
	
	title = Label(text="naslov")
	title.place(x=50, y=50, width=100, height=100)
	
	root.mainloop()


if __name__ == '__main__':
	main()