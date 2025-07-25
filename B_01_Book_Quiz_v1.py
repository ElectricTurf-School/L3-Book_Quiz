import csv
import random
from functools import partial
from tkinter import *


def round_ans(val):
    """
    Rounds temperatures to the nearest degree
    :param val: Number to be rounded
    :return: Number to the nearest degree
    """
    return int("{:.0f}".format((val * 2 + 1) // 2))


def get_questions():
    """
    returns all csv rows but also gets rid of the
    first row which shows what the column is for
    """
    file = open("books_data_v2.csv", "r")
    all_questions = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_questions.pop(0)


def get_round_questions():
    """
    Gets 4 random questions from the csv
    """
    file = open("famous_books_authors(books).csv", "r")
    all_questions = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_questions.pop(0)

    round_questions = []

    while len(round_questions) < 4:
        potential_question = random.choice(all_questions)

        if potential_question[1] not in round_questions:
            round_questions.append(potential_question)

    return round_questions


class Play:
    def __init__(self, how_many):

        self.correct_button = None
        self.round_question = None
        self.picked_question = None
        self.target_score = IntVar()

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_won = IntVar()

        self.round_quiz_list = []
        self.score = 0
        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box, bg='white')
        self.game_frame.grid()

        self.row_count = 1

        self.top_bar_frame = Frame(self.game_frame, bg='')
        self.top_bar_frame.grid(row=self.new_row())

        play_label_list = [
            [self.top_bar_frame, f"Round 0 out of {self.rounds_wanted.get()}", None, 0, 0],
            [self.top_bar_frame, f"Question", None, 1, 0],

        ]
        label_ref_list = []

        for item in play_label_list:
            make_label = Label(item[0], text=item[1], bg=item[2], font=("Arial", 16, "bold"), fg="#000000")
            make_label.grid(row=item[0] == self.game_frame and self.new_row() or item[3], column=item[4])
            label_ref_list.append(make_label)

        self.heading_label = label_ref_list[0]
        self.question_label = label_ref_list[1]

        self.answer_frame = Frame(self.game_frame, bg='')
        self.answer_frame.grid(row=self.new_row())
        self.options_frame = Frame(self.game_frame, bg='')
        self.options_frame.grid(row=self.new_row())

        # (Frame | Text | bg | Command | Width | Row | Column)
        control_button_list = [
            [self.options_frame, "Next Round", "#0057D8", self.new_round, 21, 0, 2],
            [self.options_frame, "Hints", "#FF8000", self.to_hint, 10, 0, 1],
            [self.options_frame, "Stats", "#333333", self.to_stats, 10, 0, 3],
            [self.game_frame, f"End", "#6b30c7", self.close_play, 0, 520, 10, 'absolute']
        ]

        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=("Arial", 16, "bold"), fg="#FFFFFF", width=item[4])
            try:
                if item[7] == 'absolute':
                    make_control_button.place(x=item[5], y=item[6])
            except IndexError:
                make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        self.next_button = control_ref_list[0]
        self.to_hint_button = control_ref_list[1]
        self.to_stat_button = control_ref_list[2]
        self.to_end_button = control_ref_list[3]

        self.question_button_ref = []
        self.button_color_list = ["#ff3355", "#45a3e5", "#ffc00a", "#66bf39"]
        for item in range(0, 4):  # Colors the buttons from 1 to 4 based off the list above
            self.question_button = Button(self.answer_frame, font=("Arial", 12), bg=self.button_color_list[item],
                                          text="question Name", width=30,
                                          command=partial(self.round_results, item), fg="#000")
            self.question_button.grid(row=item // 2, column=item % 2, padx=10, pady=10)
            self.question_button_ref.append(self.question_button)

        self.new_round()

    def new_row(self):
        """
        Makes/adds a new row so that if I add another row in between.
        I don't have to set every row a different number
        """
        self.row_count += 1
        return self.row_count - 1

    def new_round(self):
        """
        Chooses four colors, works out the median for score to beat. Configured buttons with chosen colors
        """
        for count, item in enumerate(self.question_button_ref):
            item.config(bg=self.button_color_list[count])

        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        self.round_quiz_list = get_round_questions()

        self.heading_label.config(text=f"Round {rounds_played} out of {self.rounds_wanted.get()}", bg='white')
        self.picked_question = random.choice(self.round_quiz_list)
        self.round_question = self.picked_question[1]

        self.question_label.config(text="What did " + self.round_question + " write?", bg='white')
        for count, item in enumerate(self.question_button_ref):
            correct = self.picked_question == self.round_quiz_list[count]  # Check if button is the correct answer
            item.config(text=self.round_quiz_list[count][0], state=NORMAL,
                        command=partial(self.round_results, correct, item))
            self.correct_button = correct and item or self.correct_button
        self.next_button.config(state=DISABLED)

    def round_results(self, correct, button):
        """check if the answer is correct or wrong.
        Check if the rounds wanted are equal to rounds played to end the game
        Enables and disables buttons"""
        if correct:
            result_text = f"Success you earned a point"
            result_bg = "#82B366"
            self.score += 1
        else:
            result_text = f"Oops you did not get the answer right."
            result_bg = "#F8CECC"

        button.config(bg="#B2BEB5")
        for item in self.question_button_ref:
            if item == self.correct_button:
                item.config(bg="#90EE90")
            elif button == item:
                item.config(bg="#F8CECC")
            else:
                item.config(bg="#B2BEB5")

        self.question_label.config(text=result_text, bg=result_bg)
        self.next_button.config(state=NORMAL)
        self.to_stat_button.config(state=NORMAL)

        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()
        if rounds_played == rounds_wanted:
            self.next_button.config(text="Play again", command=self.close_play)
            self.to_end_button.config(state=DISABLED, command=self.close_play)

            for item in self.question_button_ref:
                item.config(state=DISABLED)
            return

        for item in self.question_button_ref:
            item.config(state=DISABLED)

    def close_play(self):
        # reshow root (i.e.: choose rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()

    def to_hint(self):
        """
        Displays hints for playing
        :return:
        """
        DisplayHints(self)

    def to_stats(self):
        """
        Displays stats for playing
        :return:
        """

        stats_bundle = [self.score, self.rounds_played.get(), self.rounds_wanted.get()]
        Stats(self, stats_bundle)


class StartGame:
    """
    Initial Game interface (asks users how many rounds they
    would like to play)
    """

    def __init__(self):
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

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"))
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        self.play_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#6b30c7", text="Play", width=10, command=self.check_rounds)
        self.play_button.grid(row=1, column=0)

    def check_rounds(self):
        """checks if the user has not inputted lower than 1 or a non int into the round picking input
        Goes to the game if the conditions meet"""
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


class DisplayHints:
    def __init__(self, partner):
        """
        Tells you how to play the game in a smaller window
        """
        # setup dialogue box
        background = "#ffe6cc"
        self.hint_box = Toplevel()

        partner.to_hint_button.config(state=DISABLED)

        self.hint_box.protocol("WM_DELETE_WINDOW", partial(self.close_hint, partner))

        self.hint_frame = Frame(self.hint_box, width=300, height=200)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame, text="hint / Info", font=("Arial", 14, "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "The score for each answer relates to if you get the question right or wrong.\n" \
                    "Remember, there is only 1 answer - which is the best possible score from a single question."

        self.hint_text_label = Label(self.hint_frame, text=hint_text, wraplength=350, justify="left")
        self.hint_text_label.grid(row=1, pady=10)

        self.dismiss_button = Button(self.hint_frame, font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600", fg="#FFFFFF",
                                     command=partial(self.close_hint, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolor_list = [self.hint_frame, self.hint_heading_label, self.hint_text_label]

        for item in recolor_list:
            item.config(bg=background)

    def close_hint(self, partner):
        partner.to_hint_button.config(state=NORMAL)
        self.hint_box.destroy()


class Stats:
    """
    Shows user their round statistics in a window such as wins, average, and total, and shows them if they have 100% or 0%
    """
    def __init__(self, partner, all_stats_info):
        rounds_won = all_stats_info[0]
        rounds_played = all_stats_info[1]
        rounds_wanted = all_stats_info[2]

        # setup dialogue box
        self.stats_box = Toplevel()

        partner.to_stat_button.config(state=DISABLED)

        self.stats_box.protocol("WM_DELETE_WINDOW", partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200)
        self.stats_frame.grid()

        success_rate = rounds_won / rounds_played * 100

        whole_score = rounds_won / rounds_wanted * 100
        success_string = (f"Success rate {rounds_won} / {rounds_played}"
                          f" ({success_rate:.0f}%)")
        rounds_played_string = f"Answered {rounds_played} out of {rounds_wanted} Questions"
        total_score_string = f"Total Score {rounds_won}"

        if rounds_won == rounds_wanted:
            comment_string = "Amazing! you got the highest possible score!" # if the win count matches rounds wanted
            comment_color = "#D5E8D4"
        elif rounds_won == 0:
            comment_string = ("Oops - You (the looser) lost every round! " # if the win count is 0
                              "You might want to look at the hints!")
            comment_color = "#F8CECC"
        else:
            comment_string = ""
            comment_color = "#F0F0F0"

        average_score_string = f"Whole Score: {rounds_won}/{rounds_wanted} ({whole_score:.0f}%)\n"

        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")
        comment_font = ("arial", "13")

        all_stats_strings = [
            ["Statistics", heading_font, ""],
            [rounds_played_string, normal_font, "N"],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            [comment_string, comment_font, "W"],
            ["\nRound Stats", heading_font, "w"],
            [average_score_string, normal_font, "W"]
        ]

        stats_label_ref_list = []

        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="center", padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        stats_comment_label = stats_label_ref_list[4]
        stats_comment_label.config(bg=comment_color)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#CC6600", fg="#FFFFFF",
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=9, padx=10, pady=10)

    def close_stats(self, partner):
        partner.to_stat_button.config(state=NORMAL)
        self.stats_box.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title("Book Quiz")
    StartGame()
    root.mainloop()
