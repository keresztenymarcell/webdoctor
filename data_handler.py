import csv

DATA_FILE_PATH_questions = 'sample_data/question.csv'
DATA_FILE_PATH_answers = 'sample_data/answer.csv'

QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']


def open_csvfile(filepath):
    with open(filepath, newline='') as csvfile:
        read_csvfile = list(csv.DictReader(csvfile))
        return read_csvfile


def sort_questions(filepath, sorting_direction=False, sorting_key='submission_time'):
    read_csvfile = open_csvfile(filepath)
    sorted_listofdict = sorted(read_csvfile, key=lambda x: x[sorting_key], reverse=sorting_direction)
    return sorted_listofdict
