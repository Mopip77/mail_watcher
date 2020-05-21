import os
import json

from utils.path_utils import path_utils


NEED_FIELDS = ['subject', 'msg', 'smtp', 'receivers']


# 通过邮件的绝对路径解析邮件，除了检查所需字段外
# 还会设置该邮件文件名:filename，该邮件路径:path, 该邮件使用smtp配置的绝对路径:smtp_path供后续使用
def parse(mail_paths):
    mails = []

    for mail_path in mail_paths:
        if not os.path.isfile(mail_path):
            raise RuntimeError("发送邮件路径{}不存在".format(mail_path))

        with open(mail_path) as f:
            try:
                mail = json.load(f)
            except:
                raise RuntimeError("邮件{} 的json格式错误".format(mail_path))

            if not all(field in mail for field in NEED_FIELDS):
                raise RuntimeError("邮件{} 的缺少所需要的字段".format(mail_path))

            mail['filename'] = mail_path[mail_path.rfind("/") + 1:]
            mail['path'] = mail_path
            mail['smtp_path'] = '{}/{}.json'.format(path_utils.smtp_config_folder_path, mail['smtp'])
            mails.append(mail)

    return mails
