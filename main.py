import os
import sys
import tkinter as tk
from random import randint


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)


class App:
	def __init__(self):
		self.game_over = False
		self.game_mode = "easy"
		self.digits_input = []
		self.digits_correct = []
		self.digits_on_canvas = []

		self.root = tk.Tk()
		self.root.geometry(f'500x340'
		                   f'+{self.root.winfo_screenwidth() // 2 - 250}'
		                   f'+{self.root.winfo_screenheight() // 2 - 170}')
		self.root.resizable(False, False)
		self.root.title('NumGuessr')
		self.root.iconbitmap(resource_path("resources/num-icon.ico"))
		self.root.config(background="#9ECFC2")

		self.title = tk.Label(self.root, text="NumGuessr", font=("Helvetica", 30, "italic", "bold"),
		                      background="#9ECFC2", activebackground="#9ECFC2",
		                      foreground="white", activeforeground="white",
		                      borderwidth=0, highlightthickness=0)
		self.title.place(x=0, y=0, width=500, height=85)

		self.difficulty_easy = tk.Label(self.root, text="Easy", font=("Helvetica", 18, "bold"), cursor="hand2",
		                                background="#6E9087", activebackground="#6E9087",
		                                foreground="white", activeforeground="white",
		                                highlightcolor="white", highlightbackground="white",
		                                highlightthickness=5, borderwidth=0)
		self.difficulty_easy.place(x=65, y=278, width=120, height=40)
		self.difficulty_easy.bind("<Enter>", lambda event: self.difficulty_easy.config(highlightthickness=5) if self.game_mode != "easy" else None)
		self.difficulty_easy.bind("<Leave>", lambda event: self.difficulty_easy.config(highlightthickness=2) if self.game_mode != "easy" else None)

		self.difficulty_medium = tk.Label(self.root, text="Medium", font=("Helvetica", 18, "bold"), cursor="hand2",
		                                  background="#6E9087", activebackground="#6E9087",
		                                  foreground="white", activeforeground="white",
		                                  highlightcolor="white", highlightbackground="white",
		                                  highlightthickness=2, borderwidth=0)
		self.difficulty_medium.place(x=190, y=278, width=120, height=40)
		self.difficulty_medium.bind("<Enter>", lambda event: self.difficulty_medium.config(highlightthickness=5) if self.game_mode != "medium" else None)
		self.difficulty_medium.bind("<Leave>", lambda event: self.difficulty_medium.config(highlightthickness=2) if self.game_mode != "medium" else None)

		self.difficulty_hard = tk.Label(self.root, text="Hard", font=("Helvetica", 18, "bold"), cursor="hand2",
		                                background="#6E9087", activebackground="#6E9087",
		                                foreground="white", activeforeground="white",
		                                highlightcolor="white", highlightbackground="white",
		                                highlightthickness=2, borderwidth=0)
		self.difficulty_hard.place(x=315, y=278, width=120, height=40)
		self.difficulty_hard.bind("<Enter>", lambda event: self.difficulty_hard.config(highlightthickness=5) if self.game_mode != "hard" else None)
		self.difficulty_hard.bind("<Leave>", lambda event: self.difficulty_hard.config(highlightthickness=2) if self.game_mode != "hard" else None)

		self.difficulty_easy.bind("<Button-1>", lambda event: self.change_difficulty("easy"))
		self.difficulty_medium.bind("<Button-1>", lambda event: self.change_difficulty("medium"))
		self.difficulty_hard.bind("<Button-1>", lambda event: self.change_difficulty("hard"))

		self.digits_canvas = tk.Canvas(self.root, background="#9ECFC2", highlightthickness=0, borderwidth=0)
		self.digits_canvas.place(x=0, y=100, height=60, width=500)

		self.restart_img_small = tk.PhotoImage(file=resource_path("resources/restart-small.png"))
		self.restart_img_big = tk.PhotoImage(file=resource_path("resources/restart-big.png"))
		self.restart = tk.Label(self.root, image=self.restart_img_small, cursor="hand2",
		                        background="#9ECFC2", activebackground="#9ECFC2",
		                        borderwidth=0, highlightthickness=0)
		self.restart.place(x=0, y=0, height=45, width=45)
		self.restart.bind("<Enter>", lambda event: self.restart.config(image=self.restart_img_big))
		self.restart.bind("<Leave>", lambda event: self.restart.config(image=self.restart_img_small))
		self.restart.bind("<ButtonRelease-1>", lambda event: self.new_game())

		self.correct_digits = tk.Label(self.root, text="Correct digits: ", font=("Helvetica", 18, "bold"),
		                               background="#9ECFC2", activebackground="#9ECFC2",
		                               foreground="white", activeforeground="white",
		                               borderwidth=0, highlightthickness=0,
		                               anchor="e")
		self.correct_digits.place(x=0, y=210, width=195, height=30)

		self.correct_places = tk.Label(self.root, text="Correct places: ", font=("Helvetica", 18, "bold"),
		                               background="#9ECFC2", activebackground="#9ECFC2",
		                               foreground="white", activeforeground="white",
		                               borderwidth=0, highlightthickness=0,
		                               anchor="e")
		self.correct_places.place(x=0, y=240, width=195, height=30)

		self.tries = tk.Label(self.root, text="Tries: ", font=("Helvetica", 18, "bold"),
		                      background="#9ECFC2", activebackground="#9ECFC2",
		                      foreground="white", activeforeground="white",
		                      borderwidth=0, highlightthickness=0,
		                      anchor="e")
		self.tries.place(x=0, y=180, width=195, height=30)

		self.correct_digits_num = tk.Label(self.root, text="0", font=("Helvetica", 18, "bold"),
		                                   background="#9ECFC2", activebackground="#9ECFC2",
		                                   foreground="white", activeforeground="white",
		                                   borderwidth=0, highlightthickness=0,
		                                   anchor="w")
		self.correct_digits_num.place(x=200, y=210, width=300, height=30)

		self.correct_places_num = tk.Label(self.root, text="0", font=("Helvetica", 18, "bold"),
		                                   background="#9ECFC2", activebackground="#9ECFC2",
		                                   foreground="white", activeforeground="white",
		                                   borderwidth=0, highlightthickness=0,
		                                   anchor="w")
		self.correct_places_num.place(x=200, y=240, width=300, height=30)

		self.tries_num = tk.Label(self.root, text="0", font=("Helvetica", 18, "bold"),
		                          background="#9ECFC2", activebackground="#9ECFC2",
		                          foreground="white", activeforeground="white",
		                          borderwidth=0, highlightthickness=0,
		                          anchor="w")
		self.tries_num.place(x=200, y=180, width=300, height=30)

		self.end_status = tk.Label(self.root, text="", font=("Helvetica", 18, "bold"),
		                           background="#9ECFC2", activebackground="#9ECFC2",
		                           foreground="green", activeforeground="green",
		                           borderwidth=0, highlightthickness=0,
		                           anchor=tk.CENTER)
		self.end_status.place(y=180, height=90, width=225, x=275)

		self.controls = tk.Label(self.root, text="CONTROLS: | "
		                                         "Numbers = enter digits | "
		                                         "Enter = check entry | "
		                                         "BackSpace = delete last digit | "
		                                         "Delete = delete all digits",
		                         font=("Helvetica", 7, "italic"), anchor=tk.CENTER,
		                         background="#9ECFC2", activebackground="#9ECFC2",
		                         foreground="white", activeforeground="white",
		                         borderwidth=0, highlightthickness=0)
		self.controls.place(x=0, y=323, width=500, height=12)

		self.root.bind("<KeyPress>", lambda event: self.key_press(event))

		self.new_game()

		self.root.mainloop()

	def key_press(self, event):
		if not self.game_over:
			try:
				indeks = self.digits_input.index(None)
			except ValueError:
				indeks = len(self.digits_input)

			match event.keysym:
				case "BackSpace":
					if indeks != 0:
						self.digits_input[indeks - 1] = None
						self.end_status.config(text="")
				case "Delete":
					self.digits_input = [None for _ in range(len(self.digits_correct))]
					self.end_status.config(text="")
				case "Return":
					if indeks == len(self.digits_input):
						result = self.check_guess()
						self.correct_digits_num.config(text=str(result[0]))
						self.correct_places_num.config(text=str(result[1]))
						self.tries_num.config(text=str(int(self.tries_num["text"]) + 1))
						if result[2]:
							self.end_status.config(text="Success!", foreground="green", activeforeground="green")
							self.game_over = True
						else:
							self.end_status.config(text="Wrong!", foreground="red", activeforeground="red")
				case _:
					try:
						self.digits_input[indeks] = int(event.keysym)
						self.end_status.config(text="")
					except (IndexError, ValueError):
						pass

			for digit, tekst in zip(self.digits_on_canvas, self.digits_input):
				self.digits_canvas.itemconfig(digit, text=str(tekst) if tekst is not None else "*")

	def new_game(self):
		self.end_status.config(text="")
		self.correct_digits_num.config(text="0")
		self.correct_places_num.config(text="0")
		self.tries_num.config(text="0")

		self.game_over = False
		self.digits_canvas.delete("all")

		match self.game_mode:
			case "easy":
				num_len = 4
			case "medium":
				num_len = 6
			case "hard":
				num_len = 8
			case _:
				num_len = 0

		digits_coords = []

		number = randint(10 ** (num_len - 1), int("".join(map(str, [9 for _ in range(num_len)]))))
		number_digits = [int(x) for x in str(number)]
		len_number = len(number_digits)

		start_coord = (500 - (len_number * 35 + (len_number - 1) * 15)) // 2
		line_or_space = True
		for i in range(2 * len_number - 1):
			if line_or_space:
				self.digits_canvas.create_line(start_coord, 50, start_coord + 35, 50, fill="white", width=4)
				digits_coords.append(start_coord + 17)
				line_or_space = False
				start_coord += 35
			else:
				start_coord += 15
				line_or_space = True

		self.digits_on_canvas = []
		self.digits_correct = number_digits
		self.digits_input = [None for _ in range(num_len)]
		for i in range(len(digits_coords)):
			self.digits_on_canvas.append(self.digits_canvas.create_text(
				digits_coords[i], 55, text="*", font=("Helvetica", 40, "bold"),
				fill="white", activefill="white", anchor="s"
			))

	def change_difficulty(self, new_difficulty):
		if new_difficulty != self.game_mode:
			self.game_mode = new_difficulty

			match self.game_mode:
				case "easy":
					self.difficulty_easy.config(highlightthickness=5)
					self.difficulty_medium.config(highlightthickness=2)
					self.difficulty_hard.config(highlightthickness=2)
				case "medium":
					self.difficulty_easy.config(highlightthickness=2)
					self.difficulty_medium.config(highlightthickness=5)
					self.difficulty_hard.config(highlightthickness=2)
				case "hard":
					self.difficulty_easy.config(highlightthickness=2)
					self.difficulty_medium.config(highlightthickness=2)
					self.difficulty_hard.config(highlightthickness=5)

			self.new_game()

	def check_guess(self):
		guess = self.digits_input.copy()
		correct = self.digits_correct.copy()

		correct_digits = 0
		correct_places = 0
		for i, j in zip(guess, correct):
			if i == j:
				correct_places += 1

		victory = True if len(correct) == correct_places else False
		while len(guess) > 0:
			if guess[0] in correct:
				correct_digits += 1
				correct.pop(correct.index(guess[0]))
			guess.pop(0)

		return correct_digits, correct_places, victory


def main():
	App()


if __name__ == '__main__':
	main()
