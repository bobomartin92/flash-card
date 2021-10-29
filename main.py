from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_dict = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_dict = original_data.to_dict(orient="records")
else:
    words_dict = data.to_dict(orient="records")


def next_card():
    global current_card, flip

    window.after_cancel(flip)
    current_card = random.choice(words_dict)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, fill="black", text=current_card["French"])
    canvas.itemconfig(card_background, image=front_card)
    flip = window.after(3000, flip_card)


def flip_card():

    canvas.itemconfig(card_background, image=back_card)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


def is_known():
    words_dict.remove(current_card)
    new_data = pandas.DataFrame(words_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 265, image=front_card)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


unknown_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_image, bd=0, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, bd=0, highlightthickness=0, command=is_known)
check_button.grid(column=1, row=1)

next_card()

window.mainloop()
