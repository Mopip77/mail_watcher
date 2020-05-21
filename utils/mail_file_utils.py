import shutil
import os

from utils.path_utils import path_utils


def move_sent_mails(mails):
    data_path = path_utils.data_root_path

    for mail in mails:
        new_file_path = os.path.join(path_utils.sent_mail_folder_path, mail['sent_time'] + " " + mail['filename'])
        shutil.move(mail['path'], new_file_path)