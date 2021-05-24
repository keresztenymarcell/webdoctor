import csv

DATA_FILE_PATH_QUESTIONS = '/home/gyongyi/projects/ask-mate-1-python-gyongyi0888/sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = 'sample_data/answer.csv'

QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']


def open_csvfile(filepath):
    with open(filepath, newline='') as csvfile:
        read_csvfile = list(csv.DictReader(csvfile))
        return read_csvfile


def sort_questions(sorting_direction=False, sorting_key='submission_time'):
    read_csvfile = open_csvfile(DATA_FILE_PATH_QUESTIONS)
    sorted_listofdict = sorted(read_csvfile, key=lambda x: x[sorting_key], reverse=sorting_direction)
    return sorted_listofdict

# writing back to csv according to id(ascending)? + use header to make order within rows