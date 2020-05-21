#!env python3
from utils.path_utils import path_utils
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from send_mail import send_mail

import psutil
import os
import logging

WATCH_PATH = path_utils.mail_folder_path
PID_LOG_PATH = path_utils.root_path + '/pid.log'


class MailMonitorHandler(FileSystemEventHandler):
    def __init__(self, **kwargs):
        super(MailMonitorHandler, self).__init__(**kwargs)
        self._watch_path = WATCH_PATH
        self.logger = logging.getLogger(MailMonitorHandler.__name__)
        self.__init_log()

    def __init_log(self):
        self.logger.setLevel(logging.INFO)
        log_path = path_utils.data_root_path + '/mail.log'
        fh = logging.FileHandler(log_path, mode='a', encoding='utf-8')
        fh.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s-[%(levelname)s]: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            self.__send_mail(file_path)

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            self.__send_mail(file_path)

    def __send_mail(self, mail_path):
        if mail_path.endswith(".json"):
            self.logger.info("尝试发送：" + mail_path)
            try:
                send_mail([mail_path])
                self.logger.info("邮件{}发送成功".format(mail_path))
            except Exception as e:
                self.logger.error(e)


def write_pid():
    pid = os.getpid()
    fp = open(PID_LOG_PATH, 'w')
    fp.write(str(pid))
    fp.close()


def read_pid():
    if os.path.exists(PID_LOG_PATH):
        fp = open(PID_LOG_PATH, 'r')
        pid = fp.read()
        fp.close()
        return pid
    else:
        return False


def check_watcher_not_running():
    pid = read_pid()
    pid = int(pid)
    if pid:
        running_pid = psutil.pids()
        if pid in running_pid:
            raise RuntimeError("该程序已经运行过，PID: {}".format(pid))
        else:
            write_pid()
    else:
        write_pid()


if __name__ == '__main__':
    check_watcher_not_running()

    monitor = MailMonitorHandler()
    observer = Observer()
    observer.schedule(monitor, path=WATCH_PATH, recursive=True)
    observer.start()
    observer.join()
