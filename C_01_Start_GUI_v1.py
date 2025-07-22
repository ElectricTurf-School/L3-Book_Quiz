from tkinter import *
from functools import partial


class StartGame:
    """
    Initial Game interface (asks users how many rounds they
    would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds per user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        intro_string = ("In each round you will be given a question. "
                        "your goal is to answer the questions correctly and win the round.")

        choose_string = "How many rounds do you want to play?"

        font_16_bold = ("Arial", "16", "bold")
        font_12 = ("Arial", "12")
        font_12_bold = ("Arial", "12", "bold")

        start_labels_list = [
            ["Book Quiz", font_16_bold, None, 'left'],
            [intro_string, font_12, None, 'center'],
            [choose_string, font_12_bold, "#009900", 'left']

        ]

        start_labels_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], fg=item[2], wraplength=350,
                               justify=item[3], padx=10, pady=20)
            make_label.grid(row=count)
            start_labels_ref.append(make_label)

        self.choose_label = start_labels_ref[2]
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"))
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#6b30c7", text="Play", width=10, command=self.check_rounds)
        self.play_button.grid(row=1, column=0)

    def check_rounds(self):
        rounds_wanted = self.num_rounds_entry.get()

        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                Play(rounds_wanted)
                root.withdraw()
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            self.choose_label.config(text=error, fg="#990000", font=("Arial", "10", "bold"))

            self.num_rounds_entry.config(bg="#F4CCCC")

            # Delete characters starting from the 0(th) to max(th)
            self.num_rounds_entry.delete(0, END)


class Play:
    def __init__(self, how_many):
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.game_heading_label = Label(self.game_frame, text=f"Round 0 of {how_many}", font=("Arial", "16", "bold"))
        self.game_heading_label.grid(row=0)

        self.end_game_button = Button(self.game_frame, text="End Game",
                                      font=("Arial", "16", "bold"), fg="#FFFFFF", bg="#990000", width="10",
                                      command=self.close_play)
        self.end_game_button.grid(row=1)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title("Book Quiz")
    StartGame()
    root.mainloop()
