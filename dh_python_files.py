import re
from werkzeug.utils import secure_filename
from datetime import datetime
import dh_general



def image_data_handling(UPLOAD_FOLDER, image_data, get_data, do_edit):
    if secure_filename(image_data.filename) != "":
        time = generate_timestamp()
        to_replace = {'-': '', ' ': '_', ':': ''}
        for key, value in to_replace.items():
            time = time.replace(key, value)
        get_data["image"] = time + "_" + secure_filename(image_data.filename)
        folder_route = UPLOAD_FOLDER + get_data["image"]
        image_data.save(folder_route)
    elif do_edit:
        pass
    else:
        get_data["image"] = ''


def insert_tag(target_indices, datatable, entry_index, key, phrase, tag_type):
    count = 0
    for start in target_indices:
        result = list(datatable[entry_index][key])
        result.insert((start + count * (len(f'<{tag_type}>') + len(f'</{tag_type}>'))), f'<{tag_type}>')
        result.insert((start + (count * (len(f'<{tag_type}>') + len(f'</{tag_type}>'))) + 1 + len(phrase)), f'</{tag_type}>')
        result = ''.join(result)
        datatable[entry_index][key] = result
        count += 1


def highlight_search_phrase(datatable, phrase, tag_type):
    for entry_index in range(len(datatable)):
        title_lower = datatable[entry_index]['title'].lower()
        q_message_lower = datatable[entry_index]['q_message'].lower()

        title_iter = re.finditer(phrase, title_lower)
        title_indices = [m.start(0) for m in title_iter]
        insert_tag(title_indices, datatable, entry_index, 'title', phrase, tag_type)

        q_message_iter = re.finditer(phrase, q_message_lower)
        q_message_indices = [m.start(0) for m in q_message_iter]
        insert_tag(q_message_indices, datatable, entry_index, 'q_message', phrase, tag_type)

        if datatable[entry_index]['a_message'] is not None:
            a_message_lower = datatable[entry_index]['a_message'].lower()
            a_message_iter = re.finditer(phrase, a_message_lower)
            a_message_indices = [m.start(0) for m in a_message_iter]
            insert_tag(a_message_indices, datatable, entry_index, 'a_message', phrase, tag_type)

    return datatable


def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")