import io
import json
import os

from PyPDF2 import PdfReader

BASE_PATH = "arqcp"
FILE_NAME = "arqcp.json"

questions = {
    "2021recurso_versao_a": [],
    "2021normal_versao_a": [],
    "2020normal_versao_a": [],
    "2020recurso_versao_a": [],
    "2019recurso_versao_a": [],
    "2019normal_versao_a": [],
    "2018normal_versao_a": [],
    "2018recurso_versao_a": [],
    "2017recurso_versao_a": [],
    "2017normal_versao_a": [],
    "2016normal_versao_a": [],
    "2016recurso_versao_a": [],
}

print()


def get_correct_index(line):
    line = line.strip()
    options_index = max(line.find("xo"), line.find("ox"))
    if line[options_index] == "x":
        return 0
    if line[options_index] == "o":
        return 1
    return -1


def remove_question_number(question):
    number_index = question.find(")")
    return question[number_index+1:].strip()


def extract_question(line):
    separator_index = line.find("....")
    question = ""

    if separator_index > -1:
        question = remove_question_number(line[:separator_index].strip())
    else:
        question = line.strip()

    return remove_question_number(question)


def extract_questions(text, key):
    cur_questions = []
    print("Extracting questions from " + key + " ...")

    words = text.split(" ")
    current_question_words = []
    question_number = 1

    for word in words:
        if word == str(question_number) + ")":
            line = " ".join(current_question_words)

            question = extract_question(line)
            options = ["Verdadeiro", "Falso"]
            correct_index = get_correct_index(line)
            cur_questions.append(
                {"question_number": question_number-1, "question": question, "options": options, "correct_index": correct_index})
            current_question_words = []

            question_number += 1
        current_question_words.append(word)

    line = " ".join(current_question_words)

    question = extract_question(line)
    options = ["Verdadeiro", "Falso"]
    correct_index = get_correct_index(line)
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
