import random
import csv

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


print(get_round_questions())