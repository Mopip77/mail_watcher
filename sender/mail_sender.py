from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import time_utils, mail_file_utils

import smtplib


# 批量发送邮件，并且这些邮件必须是使用同一个SMTP配置
def send_mails(mails, smtp_config, text_format='plain', print_success=False):
    if len(mails) == 0:
        return

    try:
        smtp_obj = smtplib.SMTP_SSL(smtp_config['host'], smtp_config['port'])
        smtp_obj.login(smtp_config['user'], smtp_config['pwd'])
    except:
        print("SMTP配置{} 连接SMTP服务器错误，请检查\n相关邮件为:")
        for mail in mails:
            print("  " + mail['path'])
        return

    sent_mails = []
    for mail in mails:
        sender = smtp_config['user']
        receivers = mail['receivers']

        message = MIMEText(mail['msg'], text_format, 'utf-8')
        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receivers)
        message['Subject'] = mail['subject']

        try:
            smtp_obj.sendmail(sender, receivers, message.as_string())
            mail['sent_time'] = time_utils.now_str()
            sent_mails.append(mail)
            if print_success:
                print("发送邮件{} 成功".format(mail['path']))
        except:
            print("邮件{} 发送失败，请稍后重试")

    mail_file_utils.move_sent_mails(mails)

    smtp_obj.quit()
