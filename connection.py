import csv

DATA_FILE_PATH_QUESTIONS = 'sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = 'sample_data/answer.csv'

QUESTION_KEYS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def open_csvfile(filepath):
    with open(filepath, newline='') as csvfile:
        read_csvfile = list(csv.DictReader(csvfile))
        return read_csvfile


def read_from_csv(filepath):
    input_file = csv.DictReader(open(filepath))
    database = []
    for row in input_file:
        database.append(row)

    return database
