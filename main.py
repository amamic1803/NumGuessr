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

def hover_difficulty(event, name, widget, thickness):
	global selected_gamemode
	if selected_gamemode != name:
		widget.config(highlightthickness=thickness)

def hover_restart(event, widget, img_ind, images):
	widget.config(image=images[img_ind])

def click_difficulty(event, clicked_mode, widgets, widget_ind):
	global selected_gamemode
	if clicked_mode != selected_gamemode:
		selected_gamemode = clicked_mode
		for i in range(len(widgets)):
			if i == widget_ind:
				widgets[i].config(highlightthickness=5)
			else:
				widgets[i].config(highlightthickness=2)
		new_game(None, selected_gamemode)

def click_restart(event):
	global selected_gamemode
	new_game(None, selected_gamemode)

def new_game(event, difficulty):
	global digits_canvas, digits
	digits_canvas.delete("all")

	match difficulty:
		case "easy":
			num_len = 4
		case "medium":
			num_len = 6
		case "hard":
			num_len = 8

	digits_coords = []
	number = randint(10 ** (num_len - 1), int("".join(map(str, [9 for _ in range(num_len)]))))
	number_digits = [int(x) for x in str(number)]
	len_number = len(number_digits)
	start_coord = (500 - (len_number * 35 + (len_number - 1) * 15)) // 2
	line_or_space = True
	for i in range(2 * len_number - 1):
		if line_or_space:
			digits_canvas.create_line(start_coord, 50, start_coord + 35, 50, fill="white", width=4)
			digits_coords.append(start_coord + 17)
			line_or_space = False
			start_coord += 35
		else:
			start_coord += 15
			line_or_space = True

	digits = []
	for i in range(len(digits_coords)):
		digits.append([None, number_digits[i], digits_canvas.create_text(digits_coords[i], 55, text="*", font=("Helvetica", 40, "bold"), fill="white", activefill="white", anchor="s")])

def gui():
	global digits_canvas, selected_gamemode

	root = Tk()
	root.geometry(f'500x330+{root.winfo_screenwidth() // 2 - 250}+{root.winfo_screenheight() // 2 - 165}')
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
	                        background="#6E9087", activebackground="#6E9087",
	                        foreground="white", activeforeground="white",
	                        highlightthickness=5, highlightcolor="white", highlightbackground="white",
	                        borderwidth=0)
	difficulty_easy.place(x=65, y=278, width=120, height=40)
	difficulty_easy.bind("<Enter>", lambda event: hover_difficulty(event, "easy", difficulty_easy, 5))
	difficulty_easy.bind("<Leave>", lambda event: hover_difficulty(event, "easy", difficulty_easy, 2))
	difficulty_medium = Label(text="Medium", font=("Helvetica", 18, "bold"),
	                          background="#6E9087", activebackground="#6E9087",
	                          foreground="white", activeforeground="white",
	                          highlightthickness=2, highlightcolor="white", highlightbackground="white",
	                          borderwidth=0)
	difficulty_medium.place(x=190, y=278, width=120, height=40)
	difficulty_medium.bind("<Enter>", lambda event: hover_difficulty(event, "medium", difficulty_medium, 5))
	difficulty_medium.bind("<Leave>", lambda event: hover_difficulty(event, "medium", difficulty_medium, 2))
	difficulty_hard = Label(text="Hard", font=("Helvetica", 18, "bold"),
	                        background="#6E9087", activebackground="#6E9087",
	                        foreground="white", activeforeground="white",
	                        highlightthickness=2, highlightcolor="white", highlightbackground="white",
	                        borderwidth=0)
	difficulty_hard.place(x=315, y=278, width=120, height=40)
	difficulty_hard.bind("<Enter>", lambda event: hover_difficulty(event, "hard", difficulty_hard, 5))
	difficulty_hard.bind("<Leave>", lambda event: hover_difficulty(event, "hard", difficulty_hard, 2))
	difficulty_easy.bind("<Button-1>", lambda event: click_difficulty(event, "easy", (difficulty_easy, difficulty_medium, difficulty_hard), 0))
	difficulty_medium.bind("<Button-1>", lambda event: click_difficulty(event, "medium", (difficulty_easy, difficulty_medium, difficulty_hard), 1))
	difficulty_hard.bind("<Button-1>", lambda event: click_difficulty(event, "hard", (difficulty_easy, difficulty_medium, difficulty_hard), 2))

	digits_canvas = Canvas(root,
	                       background="#9ECFC2",
	                       highlightthickness=0, borderwidth=0)
	digits_canvas.place(x=0, y=100, height=60, width=500)

	restart_img_small = PhotoImage(file=resource_path("restart-small.png"))
	restart_img_big = PhotoImage(file=resource_path("restart-big.png"))
	restart = Label(image=restart_img_small,
	                background="#9ECFC2", activebackground="#9ECFC2",
	                borderwidth=0, highlightthickness=0)
	restart.place(x=0, y=0, height=45, width=45)
	restart.bind("<Enter>", lambda event: hover_restart(event, restart, 1, (restart_img_small, restart_img_big)))
	restart.bind("<Leave>", lambda event: hover_restart(event, restart, 0, (restart_img_small, restart_img_big)))
	restart.bind("<Button-1>", lambda event: click_restart(event))

	correct_digits = Label(text="Correct digits: ", font=("Helvetica", 18, "bold"),
	                       background="#9ECFC2", activebackground="#9ECFC2",
	                       foreground="white", activeforeground="white",
	                       borderwidth=0, highlightthickness=0,
	                       anchor="e")
	correct_digits.place(x=0, y=210, width=195, height=30)
	correct_places = Label(text="Correct places: ", font=("Helvetica", 18, "bold"),
	                       background="#9ECFC2", activebackground="#9ECFC2",
	                       foreground="white", activeforeground="white",
	                       borderwidth=0, highlightthickness=0,
	                       anchor="e")
	correct_places.place(x=0, y=240, width=195, height=30)
	tries = Label(text="Tries: ", font=("Helvetica", 18, "bold"),
	              background="#9ECFC2", activebackground="#9ECFC2",
	              foreground="white", activeforeground="white",
	              borderwidth=0, highlightthickness=0,
	              anchor="e")
	tries.place(x=0, y=180, width=195, height=30)

	correct_digits_num = Label(text="0", font=("Helvetica", 18, "bold"),
	                           background="#9ECFC2", activebackground="#9ECFC2",
	                           foreground="white", activeforeground="white",
	                           borderwidth=0, highlightthickness=0,
	                           anchor="w")
	correct_digits_num.place(x=200, y=210, width=300, height=30)
	correct_places_num = Label(text="0", font=("Helvetica", 18, "bold"),
	                           background="#9ECFC2", activebackground="#9ECFC2",
	                           foreground="white", activeforeground="white",
	                           borderwidth=0, highlightthickness=0,
	                           anchor="w")
	correct_places_num.place(x=200, y=240, width=300, height=30)
	tries_num = Label(text="0", font=("Helvetica", 18, "bold"),
	                  background="#9ECFC2", activebackground="#9ECFC2",
	                  foreground="white", activeforeground="white",
	                  borderwidth=0, highlightthickness=0,
	                  anchor="w")
	tries_num.place(x=200, y=180, width=300, height=30)

	end_status = Label(text="", font=("Helvetica", 18, "bold"),
	                   background="#9ECFC2", activebackground="#9ECFC2",
	                   foreground="white", activeforeground="white",
	                   borderwidth=0, highlightthickness=0,
	                   anchor=CENTER)
	end_status.place(y=180, height=90, width=225, x=275)

	new_game(0, selected_gamemode)

	root.mainloop()

def main():
	global key_pressed, selected_gamemode, digits
	key_pressed = False
	selected_gamemode = "easy"
	digits = []

	gui()


if __name__ == '__main__':
	main()
