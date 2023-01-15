import json
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

# Open database connection with .env file properties
db_connection = pymysql.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USERNAME"), password=os.getenv(
    "DB_PASSWORD"), db=os.getenv("DB_DATABASE"), port=os.getenv("PORT"),  charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# prepare a cursor object using cursor() method
cursor = db_connection.cursor()

# list all .json files in the directory
json_files = [pos_json for pos_json in os.listdir(
    '.') if pos_json.endswith('.json')]

print()
for i in range(len(json_files)):
    print(f'{i+1}. {json_files[i]}')

print("Select the file you want to import to database: ", end="")
file_index = int(input())-1

if file_index < 0 or file_index > len(json_files):
    print("Invalid file index")
    exit()

file = json_files[file_index]
print(file)

subject = file.split('.')[0]

# Open and read the file as a single buffer
fd = open(file, 'r')
json_data = json.load(fd)

print("Importing data to database...")

# Iterate over the data and insert values into the table
for exam in json_data:
    print(exam)
    for question in json_data[exam]:
        print(question)
        if question['correct_index'] == -1:
            continue
        if len(question['question']) > 255:
            continue

        # get subject id
        sql = "SELECT `id` FROM `subjects` WHERE `name` = %s"
        cursor.execute(sql, (subject))
        subject_id = cursor.fetchone()['id']

        # insert question
        sql = "INSERT INTO `questions` (`question`, `image`, `correct_option`, `exam`, `subject_id`, `question_type_id`) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (question['question'], '',
                       question['correct_index'], exam, int(subject_id), 1))

        # insert options
        question_id = cursor.lastrowid
        i = 1
        for option in question['options']:
            sql = "INSERT INTO `options` (`name`, `order`, `question_id`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (option, i, question_id))
            i += 1

print("Data imported successfully")
# Commit your changes in the database
db_connection.commit()
