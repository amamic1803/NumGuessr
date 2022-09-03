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

def hover_thickness(event, name, widget, thickness):
	global selected_gamemode
	if selected_gamemode != name:
		widget.config(highlightthickness=thickness)

def difficulty_change(event, clicked_mode, widgets, widget_ind):
	global selected_gamemode
	if clicked_mode != selected_gamemode:
		selected_gamemode = clicked_mode
		for i in range(len(widgets)):
			if i == widget_ind:
				widgets[i].config(highlightthickness=5)
			else:
				widgets[i].config(highlightthickness=2)
		print(selected_gamemode)
		new_game(None, selected_gamemode)

def new_game(event, difficulty):
	global digits_canvas
	digits_canvas.delete("all")

	match difficulty:
		case "easy":
			num_len = 4
		case "medium":
			num_len = 6
		case "hard":
			num_len = 8

	digits_coords = []

	number = randint(10 ** (num_len - 1), int("".join(map(str, [9 for i in range(num_len)]))))
	number_digits = [int(x) for x in str(number)]
	len_number = len(number_digits)
	start_coord = (500 - (len_number * 30 + (len_number - 1) * 11)) // 2
	line_or_space = True
	for i in range(2 * len_number - 1):
		if line_or_space:
			digits_canvas.create_line(start_coord, 40, start_coord + 30, 40, fill="white", width=4)
			digits_coords.append(start_coord + 14)
			line_or_space = False
			start_coord += 30
		else:
			start_coord += 11
			line_or_space = True

def GUI():
	global digits_canvas, selected_gamemode

	root = Tk()
	root.geometry(f'500x500+{root.winfo_screenwidth() // 2 - 250}+{root.winfo_screenheight() // 2 - 250}')
	root.resizable(False, False)
	root.title('NumGuessr')
	root.iconbitmap(resource_path("icon.ico"))
	root.config(background="#9ECFC2")

	root.bind(f"<KeyPress>", lambda event: key_press(event))
	root.bind(f"<KeyRelease>", lambda event: key_release(event))

	title = Label(text="NumGuessr", font=("Helvetica", 30, "italic", "bold"),
	              background="#9ECFC2", activebackground="#9ECFC2",
	              foreground="white", activeforeground="white",
	              borderwidth=0, highlightthickness=0)
	title.place(x=0, y=0, width=500, height=85)

	difficulty_easy = Label(text="Easy", font=("Helvetica", 18, "bold"),
	                        background="#9ECFC2", activebackground="#9ECFC2",
	                        foreground="white", activeforeground="white",
	                        highlightthickness=5, highlightcolor="white", highlightbackground="white",
	                        borderwidth=0)
	difficulty_easy.place(x=65, y=85, width=120, height=40)
	difficulty_easy.bind("<Enter>", lambda event: hover_thickness(event, "easy", difficulty_easy, 5))
	difficulty_easy.bind("<Leave>", lambda event: hover_thickness(event, "easy", difficulty_easy, 2))
	difficulty_medium = Label(text="Medium", font=("Helvetica", 18, "bold"),
	                          background="#9ECFC2", activebackground="#9ECFC2",
	                          foreground="white", activeforeground="white",
	                          highlightthickness=2, highlightcolor="white", highlightbackground="white",
	                          borderwidth=0)
	difficulty_medium.place(x=190, y=85, width=120, height=40)
	difficulty_medium.bind("<Enter>", lambda event: hover_thickness(event, "medium", difficulty_medium, 5))
	difficulty_medium.bind("<Leave>", lambda event: hover_thickness(event, "medium", difficulty_medium, 2))
	difficulty_hard = Label(text="Hard", font=("Helvetica", 18, "bold"),
	                        background="#9ECFC2", activebackground="#9ECFC2",
	                        foreground="white", activeforeground="white",
	                        highlightthickness=2, highlightcolor="white", highlightbackground="white",
	                        borderwidth=0)
	difficulty_hard.place(x=315, y=85, width=120, height=40)
	difficulty_hard.bind("<Enter>", lambda event: hover_thickness(event, "hard", difficulty_hard, 5))
	difficulty_hard.bind("<Leave>", lambda event: hover_thickness(event, "hard", difficulty_hard, 2))

	difficulty_easy.bind("<Button-1>", lambda event: difficulty_change(event, "easy", [difficulty_easy, difficulty_medium, difficulty_hard], 0))
	difficulty_medium.bind("<Button-1>", lambda event: difficulty_change(event, "medium", [difficulty_easy, difficulty_medium, difficulty_hard], 1))
	difficulty_hard.bind("<Button-1>", lambda event: difficulty_change(event, "hard", [difficulty_easy, difficulty_medium, difficulty_hard], 2))

	digits_canvas = Canvas(root,
	                       background="blue", #"#9ECFC2",
	                       highlightthickness=0, borderwidth=0)
	digits_canvas.place(x=0, y=250, height=50, width=500)

	restart_img_small = PhotoImage(file=resource_path("restart-small.png"))
	restart_img_big = PhotoImage(file=resource_path("restart-big.png"))

	restart = Label(image=restart_img_small,
	                background="#9ECFC2", activebackground="#9ECFC2",
	                borderwidth=0, highlightthickness=0)
	restart.place(x=0, y=0, height=45, width=45)

	new_game(0, selected_gamemode)

	root.mainloop()

def main():
	global key_pressed, selected_gamemode
	key_pressed = False
	selected_gamemode = "easy"

	GUI()


if __name__ == '__main__':
	main()
