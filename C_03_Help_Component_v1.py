from tkinter import *
from functools import partial


class DisplayHints:
    def __init__(self, partner):
        # setup dialogue box
        background = "#ffe6cc"
        self.hint_box = Toplevel()

        partner.to_hint_button.config(state=DISABLED)

        self.hint_box.protocol("WM_DELETE_WINDOW", partial(self.close_hint, partner))

        self.hint_frame = Frame(self.hint_box, width=300, height=200)
        self.hint_frame.grid()

        self.hint_heading_label = Label(self.hint_frame, text="hint / Info", font=("Arial", "14", "bold"))
        self.hint_heading_label.grid(row=0)

        hint_text = "The score for each color relates to it's hexadecimal code.\n" \
                    "Remember, the hex code for white is #FFFFFF - which is the best possible score.\n" \
                    "The first color in the code is red, so if you had to choose between \n" \
                    "red (#FF0000), Green (#00FF00) and blue (#0000FF), then red would be the best choice."

        self.hint_text_label = Label(self.hint_frame, text=hint_text, wraplength=350, justify="left")
        self.hint_text_label.grid(row=1, pady=10)

        self.dismiss_button = Button(self.hint_frame, font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600", fg="#FFFFFF",
                                     command=partial(self.close_hint, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolor_list = [self.hint_frame, self.hint_heading_label, self.hint_text_label]

        for item in recolor_list:
            item.config(bg=background)

    def close_hint(self, partner):
        partner.to_hint_button.config(state=NORMAL)
        self.hint_box.destroy()


class StartGame:

    def __init__(self):
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.to_hint_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                     fg="#FFFFFF", bg="#CC6600", text="Hint", width=10, command=self.begin)
        self.to_hint_button.grid(row=1, column=0)

    def begin(self):
        DisplayHints(self)


if __name__ == '__main__':
    root = Tk()
    root.title("Book Quiz")
    StartGame()
    root.mainloop()
