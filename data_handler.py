import connection

QUESTIONS_HEADER = ['Id', 'Submission Time', 'View Number', 'Vote Number', 'Title', 'Message', 'Image']
ANSWERS_HEADER = ['Id', 'Submission Time', 'Vote Number', 'Question Id', 'Message', 'Image']


def sort_questions(sorting_direction=False, sorting_key='submission_time'):
    read_csvfile = connection.open_csvfile(connection.DATA_FILE_PATH_QUESTIONS)
    sorted_listofdict = sorted(read_csvfile, key=lambda x: x[sorting_key], reverse=sorting_direction)
    return sorted_listofdict

# writing back to csv according to id(ascending)? + use QUESTION_KEYS/ANSWER_KEYS to make order within rows