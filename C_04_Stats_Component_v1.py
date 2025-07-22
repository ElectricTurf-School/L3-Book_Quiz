from tkinter import *
from functools import partial

from Tools.scripts.fixcid import wanted


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

        start_labels_list = [
            ["Book Quiz", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"],

        ]

        start_labels_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], fg=item[2], wraplength=350, justify="left",
                               padx=10, pady=20)
            make_label.grid(row=count)
            start_labels_ref.append(make_label)

        self.choose_label = start_labels_ref[2]
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"))
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#333333", text="Play", width=10, command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

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
        # Score Test Data...
        self.score = 3

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_played = IntVar()
        self.rounds_played.set(how_many + 2) # Test Data

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=10)

        self.stats_stats_frame = Frame(self.game_frame)
        self.stats_stats_frame.grid(row=6)

        # (Frame | Text | bg | Command | Width | Row | Column)
        control_button_list = [
            [self.stats_stats_frame, "stats", "#333333", self.to_stats, 10, 0, 0],
        ]

        control_ref_list = []

        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=("Arial", "16", "bold"), fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        self.to_stat_button = control_ref_list[0]

    def to_stats(self):
        """
        Displays stats for playing
        :return:
        """

        stats_bundle = [self.score, self.rounds_played.get(), self.rounds_wanted.get()]
        Stats(self, stats_bundle)

    def close_play(self):
        # reshow root (ie: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


class Stats:
    def __init__(self, partner, all_stats_info):
        rounds_won = all_stats_info[0]
        rounds_wanted = all_stats_info[1]
        rounds_played = all_stats_info[2]

        # setup dialogue box
        background = "#ffe6cc"
        self.stats_box = Toplevel()

        partner.to_stat_button.config(state=DISABLED)

        self.stats_box.protocol("WM_DELETE_WINDOW", partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid()

        success_rate = rounds_won / rounds_played * 100

        average_score = rounds_won / rounds_played
        success_string = (f"Success rate {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        total_score_string = f"Total Score {rounds_won}"
        max_possible_string = f"Maximum Possible Score: {rounds_wanted }"

        if rounds_won == rounds_wanted:
            comment_string = "Amazing! you got the highest possible score!"
            comment_color = "#D5E8D4"
        elif rounds_won == 0:
            comment_string = ("Oops - You (the looser) lost every round! "
                              "You might want to look at the hints!")
            comment_color = "#F8CECC"
        else:
            comment_string = ""
            comment_color = "#F0F0F0"

        average_score_string = f"Average Score: {average_score:.0f}\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("arial", "13")

        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [max_possible_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, "w"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []

        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_color)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#333333", fg="#FFFFFF",
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=9, padx=10, pady=10)

    def close_stats(self, partner):
        partner.to_stat_button.config(state=NORMAL)
        self.stats_box.destroy()


if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
