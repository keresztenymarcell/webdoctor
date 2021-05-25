import csv

DATA_FILE_PATH_QUESTIONS = 'sample_data/question.csv'
DATA_FILE_PATH_ANSWERS = 'sample_data/answer.csv'

QUESTION_KEYS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_KEYS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def open_csvfile(filepath):
    with open(filepath, newline='') as csvfile:
        read_csvfile = list(csv.DictReader(csvfile))
        return read_csvfile

<<<<<<< HEAD

def write_files(file_path, fieldnames, data_table):
    csvfile = open(file_path, "w")
    dict_writer = csv.DictWriter(csvfile, fieldnames)
    dict_writer.writeheader()
    dict_writer.writerows(data_table)
    csvfile.close()
=======

def read_from_csv(filepath):
    input_file = csv.DictReader(open(filepath))
    database = []
    for row in input_file:
        database.append(row)

    return database
>>>>>>> 153da2886ab5dd4f810182875e59b8c7b179e7e7
