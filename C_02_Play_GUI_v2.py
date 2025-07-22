from operator import index
from tkinter import *
from functools import partial
import csv
import random


def round_ans(val):
    """
    Rounds temperatures to the nearest degree
    :param val: Number to be rounded
    :return: Number to the nearest degree
    """
    return int("{:.0f}".format((val * 2 + 1) // 2))


def get_questions():
    file = open("famous_books_authors(books).csv", "r")
    all_questions = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_questions.pop(0)


def get_round_questions():
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

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(padx=10, pady=30)

        body_font = ("Arial", "12")

        self.row_count = 1

        self.top_bar_frame = Frame(self.game_frame)
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

        self.answer_frame = Frame(self.game_frame)
        self.answer_frame.grid(row=self.new_row())
        self.options_frame = Frame(self.game_frame)
        self.options_frame.grid(row=self.new_row())

        # (Frame | Text | bg | Command | Width | Row | Column)
        control_button_list = [
            [self.options_frame, "Next Round", "#0057D8", self.new_round, 21, 0, 2],
            [self.options_frame, "Hints", "#FF8000", self.to_hint, 10, 0, 1],
            [self.options_frame, "Stats", "#333333", self.to_stats, 10, 0, 3],
            [self.game_frame, f"End", "#6b30c7", self, 0, 520, -5, 'absolute']
        ]

        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=("Arial", 16, "bold"), fg="#FFFFFF", width=item[4])
            try:
                if item[7] == 'absolute':
                    make_control_button.place(x=item[5], y=item[6])
            except:
                make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # self.next_button = control_ref_list[0]
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[1]

        self.question_button_ref = []
        self.button_color_list = ["#ff3355", "#45a3e5", "#ffc00a", "#66bf39"]
        for item in range(0, 4):
            self.question_button = Button(self.answer_frame, font=("Arial", 12), bg=self.button_color_list[item], text="question Name", width=30,
                                          command=partial(self.round_results, item), fg="#000")
            self.question_button.grid(row=item // 2, column=item % 2, padx=10, pady=10)
            self.question_button_ref.append(self.question_button)

        self.new_round()

    def new_row(self):
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

        rounds_wanted = self.rounds_wanted.get()

        self.round_quiz_list = get_round_questions()

        self.heading_label.config(text=f"Round {rounds_played} out of {self.rounds_wanted.get()}")
        print(self.round_quiz_list)
        self.picked_question = random.choice(self.round_quiz_list)
        self.round_question = self.picked_question[1]

        self.question_label.config(text="What did " + self.round_question + " write?", bg=None)
        for count, item in enumerate(self.question_button_ref):
            correct = self.picked_question == self.round_quiz_list[count] # Check if button is the correct answer
            item.config(text=self.round_quiz_list[count][0], state=NORMAL, command=partial(self.round_results, correct))
            self.correct_button = correct and item or self.correct_button
            print(self.correct_button)
        self.next_button.config(state=DISABLED)

    def round_results(self, correct):
        if correct:
            result_text = f"Success you earned a point"
            result_bg = "#82B366"
            self.score += 1
        else:
            result_text = f"Oops you did not get the answer right."
            result_bg = "#F8CECC"

        for item in self.question_button_ref:
            if self.correct_button == item:
                item.config(bg="#90EE90")
            else:
                item.config(bg="#F8CECC")

        self.question_label.config(text=result_text, bg=result_bg)
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        rounds_played = self.rounds_played.get()
        rounds_wanted = self.rounds_wanted.get()

        if rounds_played == rounds_wanted:
            self.next_button.config(state=DISABLED, text="Game Over")
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
        # DisplayHints(self)

    def to_stats(self):
        """
        Displays stats for playing
        :return:
        """

        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list, self.all_high_score_list]
        # Stats(self, stats_bundle)


class StartGame:

    def __init__(self):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.play_button = Button(self.entry_area_frame, font=('Arial', 16, 'bold'),
                                  fg="#FFFFFF", bg="#6b30c7", text="Play", width=10, command=self.begin)
        self.play_button.grid(row=1, column=0)

    def begin(self):
        Play(5)
        root.withdraw()


if __name__ == '__main__':
    root = Tk()
    root.title("Book Quiz")
    StartGame()
    root.mainloop()
