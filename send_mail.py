from sender import mail_sender
from parser import mail_parser
from utils import smtp_checker

import os
import sys


if __name__ == '__main__':
    mail_paths = sys.argv[1:]
    if len(mail_paths) == 0:
        raise RuntimeError("未指定邮件文件")

    mails = mail_parser.parse(mail_paths)
    smtp_config_paths = set([mail['smtp_path'] for mail in mails])
    smtp_config_map = smtp_checker.check_format(smtp_config_paths)

    for config_path, smtp_config in smtp_config_map.items():
        mails_using_cur_smtp_config = list(filter(lambda mail: config_path == mail['smtp_path'], mails))
        mail_sender.send_mails(mails_using_cur_smtp_config, smtp_config, print_success=True)