import csv

DATA_FILE_PATH_QUESTIONS = '/home/gyongyi/projects/ask-mate-1-python-gyongyi0888/sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = 'sample_data/answer.csv'

QUESTION_KEYS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def open_csvfile(filepath):
    with open(filepath, newline='') as csvfile:
        read_csvfile = list(csv.DictReader(csvfile))
        return read_csvfile