import json
import os
import smtplib
import socket

NEED_FIELD = ['host', 'user', 'pwd', 'port']


def check_format(smtp_config_paths, print_success=False):
    configs = {}

    for config_path in smtp_config_paths:
        if not os.path.isfile(config_path):
            raise RuntimeError("SMTP配置文件路径{}不存在".format(config_path))

        with open(config_path) as f:
            try:
                config = json.load(f)
            except:
                raise RuntimeError("配置文件{}json格式错误".format(config_path))

            if not all(field in config for field in NEED_FIELD):
                raise RuntimeError("配置文件{}缺少所需字段".format(config_path))

            if (print_success):
                print("配置文件{}格式正确".format(config_path))

            configs[config_path] = config

    return configs


def check_access(smtp_config_paths, timeout=3, print_success=False):
    configs = {}

    for config_path in smtp_config_paths:
        if not os.path.isfile(config_path):
            raise RuntimeError("SMTP配置文件路径{}不存在".format(config_path))

        with open(config_path) as f:
            try:
                config = json.load(f)
            except:
                raise RuntimeError("配置文件{}json格式错误".format(config_path))

            if not all(field in config for field in NEED_FIELD):
                raise RuntimeError("配置文件{}缺少所需字段".format(config_path))

            try:
                smtp_obj = smtplib.SMTP_SSL(config['host'], config['port'], timeout=timeout)
                smtp_obj.login(config['user'], config['pwd'])
            except socket.timeout or smtplib.SMTPConnectError:
                raise RuntimeError("配置文件{}连接SMTP服务器错误，请检查服务器端口或网络".format(config_path))
            except smtplib.SMTPAuthenticationError:
                raise RuntimeError("配置文件{}认证错误".format(config_path))

            if (print_success):
                print("配置文件{}格式正确".format(config_path))

            configs[config_path] = config

    return configs
