import os


class PathUtils:
    root_path = ""
    data_root_path = ""
    mail_folder_path = ""
    sent_mail_folder_path = ""
    smtp_config_folder_path = ""
    template_folder_path = ""

    def __init__(self):
        abs_file = os.path.realpath(__file__)
        cur_file_folder = os.path.dirname(abs_file)
        cur_file_folder = os.path.abspath(os.path.join(cur_file_folder, ".."))

        PathUtils.root_path = cur_file_folder
        PathUtils.data_root_path = cur_file_folder + '/data'
        PathUtils.mail_folder_path = self.data_root_path + '/mail'
        PathUtils.sent_mail_folder_path = self.data_root_path + '/sent-mail'
        PathUtils.smtp_config_folder_path = self.data_root_path + '/smtp-config'
        PathUtils.template_folder_path = self.data_root_path + '/template'


path_utils = PathUtils()
