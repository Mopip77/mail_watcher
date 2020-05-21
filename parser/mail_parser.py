import os
import json

from parser import template_paerser
from utils.path_utils import path_utils


NEED_FIELDS = ['subject', 'smtp', 'receivers']


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

            # msg 或者 template需要存在至少一个
            if not ('msg' in mail or all(field in mail for field in ['template', 'texts', 'imgs'])):
                raise RuntimeError("邮件{} 的缺少所需要的字段".format(mail_path))

            # 解析模板文件
            if 'template' in mail:
                mail['template_html'] = template_paerser.inject(
                    "{}/{}.html".format(path_utils.template_folder_path, mail['template']),
                    mail['texts'],
                    mail['imgs']
                )

            mail['filename'] = mail_path[mail_path.rfind("/") + 1:]
            mail['path'] = mail_path
            mail['smtp_path'] = '{}/{}.json'.format(path_utils.smtp_config_folder_path, mail['smtp'])
            mails.append(mail)

    return mails
