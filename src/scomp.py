import json
import os

BASE_PATH = 'scomp'
OUTPUT_FILE = 'scomp.json'
questions = []


def remove_question_number(question):
    index = question.find(". ")
    if index > -1 and index < 4:
        return question[index+1:].strip().split('/')[0].strip()

    return question


def sanitize_options(answers):
    sanitized_answers = []

    for answer in answers:
        sanitized_answers.append(extract_option(answer))

    return sanitized_answers


def extract_option(line):
    return line[2:].strip().split('__')[0].strip()


def get_correct_index(answers):
    i = 0
    for answer in answers:
        if answer.endswith("__X__"):
            return i
        i += 1

    return -1


def extract_questions(content):
    question_number = 1
    question = {}
    options = []

    for line in content.splitlines():
        line = line.strip()
        if line == '':
            continue

        if line.startswith(str(question_number)):
            question = {}
            options = []

            question['question'] = remove_question_number(line)
            question['options'] = options

            questions.append(question)
            question_number += 1
        else:
            options.append(line)


for filename in os.listdir(BASE_PATH):
    with open(BASE_PATH + '/' + filename, 'r') as f:
        text = f.read()
        extract_questions(text)

for question in questions:
    question['correct_index'] = get_correct_index(question['options'])
    question['options'] = sanitize_options(question['options'])

# Pretty Print JSON
json_formatted_str = json.dumps(questions, indent=2, ensure_ascii=False)
file = open(OUTPUT_FILE, "w")
file.write(json_formatted_str)

print(json_formatted_str)
