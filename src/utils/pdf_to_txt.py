import io
import os

from PyPDF2 import PdfReader

BASE_PATH = "sgrai"
FILE_NAME = "sgrai.json"

questions = []


def extract_information(pdf_path):
    with io.open(pdf_path, "rb") as f:
        pdf = PdfReader(f)

        key = pdf_path.split("/")[1].split(".")[0]
        pages_text = []

        for page in pdf.pages:
            pages_text.extend(page.extract_text())
            pages_text.append(" ")

        content = ""
        for line in "".join(pages_text).split("\n"):
            if line[0].isdigit():
                content += line.split(" ")[0]
            content += line

        # write to a new file named same as pdf but with a .txt extension
        with open("{}.txt".format(key), "w", encoding="utf-8") as text_file:
            text_file.write("".join(pages_text))


for file in os.listdir(BASE_PATH):
    extract_information(BASE_PATH + "/" + file)
