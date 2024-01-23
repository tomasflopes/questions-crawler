import json
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

FILE_PATH = "sgrai.json"

db_connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_DATABASE"),
    port=int(os.getenv("PORT")),
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)

# prepare a cursor object using cursor() method
cursor = db_connection.cursor()


# Open and read the file as a single buffer
fd = open(FILE_PATH, "r")
json_data = json.load(fd)

print("Importing data to database...")

subject_id = 8

question_type_id = 107

for question in json_data:
    print(question)
    if question["correct_index"] == -1:
        continue
    if len(question["question"]) > 255:
        print("Question too long, skipping...")
        continue
    valid = True
    for option in question["options"]:
        if len(option) > 255:
            print("Option too long, skipping...")
            valid = False
    if not valid:
        continue

    # insert question
    sql = "INSERT INTO `questions` (`question`, `image`, `correct_option`, `exam`, `subject_id`, `question_type_id`) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(
        sql,
        (
            question["question"],
            "",
            question["correct_index"] + 1,
            "scomp",
            int(subject_id),
            question_type_id,
        ),
    )

    # insert options
    question_id = cursor.lastrowid
    i = 1
    for option in question["options"]:
        sql = (
            "INSERT INTO `options` (`name`, `order`, `question_id`) VALUES (%s, %s, %s)"
        )
        cursor.execute(sql, (option, i, question_id))
        i += 1

print("Data imported successfully")
# Commit your changes in the database
db_connection.commit()
