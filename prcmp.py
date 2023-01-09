import io
import json
import os

from PyPDF2 import PdfReader

BASE_PATH = "prcmp"
FILE_NAME = "prcmp.json"

questions = {
    "2021melhoria": [],
    "2021normal": [],
    "2021recurso": [],
    "2022normal": [],
    "2022recurso": [],
    "quiz": []
}

POSSIBLE_QUESTION_DELIMITERS = [
    "... ", "... o", "… ", "? ", ":", ". ", "...", "…", ". o"]
POSSIBLE_OPTIONS_DELIMITERS = [". o", " o "]

print()


def get_options(opts):
    if opts.startswith("(a)"):
        first, rest = opts.split("(b)")
        second, rest = rest.split("(c)")
        third, forth = rest.split("(d)")
        return [first[3:].strip(), second.strip(), third.strip(), forth.strip()]
    if opts.startswith("a."):
        first, rest = opts.split("b.")
        second, rest = rest.split("c.")
        third, forth = rest.split("d.")
        return [first[2:].strip(), second.strip(), third.strip(), forth.strip()]

    for delimiter in POSSIBLE_OPTIONS_DELIMITERS:
        if len(opts.split(delimiter)) == 4:
            options = opts[1:].split(delimiter)
            return [option.strip() for option in options]
    return []


def remove_question_number(question):
    index = question.find(". ")
    if index > -1 and index < 4:
        return question[index+1:].strip()

    index = question.find(") ")
    if index > -1 and index < 4:
        return question[index+1:].strip()

    return question


def separate_question(line):
    for delimiter in POSSIBLE_QUESTION_DELIMITERS:
        if len(line.split(delimiter)) == 2:
            question = remove_question_number(line.split(delimiter)[0].strip())
            return question, get_options(line.split(delimiter)[1].strip())

    return line, []  # if no delimiter is found return the whole line


def get_correct_index(options):
    for option in options:
        if option.endswith(" X"):
            return options.index(option)
    return -1


def extract_questions(text, key):
    cur_questions = []
    print("Extracting questions from " + key + " ...")

    words = text.split(" ")
    current_question_words = []
    question_number = 1

    for word in words:
        if word == str(question_number) + "." or word == str(question_number) + ")":
            line = " ".join(current_question_words)

            question, options = separate_question(line)
            correct_index = get_correct_index(options)
            if correct_index > -1:
                options[correct_index] = options[correct_index][:-2]

            cur_questions.append(
                {"question_number": question_number-1, "question": question, "options": options, "correct_index": correct_index})
            current_question_words = []
            question_number += 1

        current_question_words.append(word)

    line = " ".join(current_question_words)

    question, options = separate_question(line)
    correct_index = get_correct_index(options)
    if correct_index > -1:
        options[correct_index] = options[correct_index][:-2]  # remove X

    cur_questions.append(
        {"question_number": question_number-1, "question": question, "options": options, "correct_index": correct_index})
    questions[key] = cur_questions[1:]


def extract_information(pdf_path):
    with io.open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)

        key = pdf_path.split('/')[1].split('.')[0]
        pages_text = []

        for page in pdf.pages:
            pages_text.extend(page.extract_text().replace('\n', ' '))
            pages_text.append(" ")

        extract_questions("".join(pages_text), key)


for file in os.listdir(BASE_PATH):
    print(file)
    extract_information(BASE_PATH + "/" + file)


# Pretty Print JSON
json_formatted_str = json.dumps(questions, indent=2, ensure_ascii=False)
file = open(FILE_NAME, "w")
file.write(json_formatted_str)

print(json_formatted_str)
