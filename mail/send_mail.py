import logging
import mimetypes
import os
import smtplib
import sys
from configparser import ConfigParser
from copy import deepcopy
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from mail.html import get_html
import wget
from datetime import datetime, time
import shutil


def _check_filters(firma_filter_def, firma_def, to_addrs_def, to_addrs1_def):
    if firma_filter_def:
        firma_filter_def = firma_filter_def.split(",")
        firma_filter_def = [i.strip() for i in firma_filter_def]
        if type(firma_filter_def) is list and len(firma_filter_def) <= 100:
            for i_pattern in firma_filter_def:
                if i_pattern.lower() in firma_def.lower():
                    return [to_addrs_def, to_addrs1_def], f"{to_addrs_def}; {to_addrs1_def}"
        else:
            logging.info("в файле email.ini возможно строка firma_filter = пустая")

    return to_addrs_def, f"{to_addrs_def}"


def process_attachment(msg, files):  # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):  # Если файл существует
            attach_file(msg, f)  # Добавляем файл к сообщению
        elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
            dir = os.listdir(f)  # Получаем список файлов в папке
            for file in dir:  # Перебираем все файлы и...
                attach_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению


def attach_file(msg, filepath):  # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)  # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:  # Если тип файла не определяется
        ctype = 'application/octet-stream'  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип

    with open(filepath, 'rb') as fp:
        file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
        file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
        encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64

    file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
    msg.attach(file)


# ----------------------------------------------------------------------
def send_email_with_attachment(e_mail,
                                     firma,
                                     full_name,
                                     cont_telefon,
                                     description,
                                     priority,
                                     message_id,
                                     http_to_attach=None,
                                     number_from_1c=''):
    """
    Send an email with an attachment
    """
    val_error = 0
    check_send_bot = False
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")
    # header = 'Content-Disposition', 'attachment; filename="%s"' % http_to_attach

    # get the config
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)

    # extract server and from_addr from config
    host = cfg.get("smtp", "server")
    FROM = cfg.get("smtp", "from")
    password = cfg.get("smtp", "passwd")
    to_addrs = cfg.get("smtp", "to_addrs")
    to_addrs1 = cfg.get("smtp", "to_addrs1")
    time_start = cfg.get("time", "time_start")
    time_end = cfg.get("time", "time_end")
    firma_filter = cfg.get("filter", "firma_filter")
    if not to_addrs:
        logging.info("Не указан основной адреса получателей в файле email.ini")
        val_error = 1
        return val_error

    to_addrs0 = to_addrs
    msg_To = f"{to_addrs}"

    try:
        obj_time_start = time.fromisoformat(time_start)
        obj_time_end = time.fromisoformat(time_end)
        res_now = datetime.now().time()
        if obj_time_start <= obj_time_end:
            if obj_time_start <= res_now <= obj_time_end:
                to_addrs0, msg_To = _check_filters(firma_filter_def=deepcopy(firma_filter),
                                                   firma_def=firma,
                                                   to_addrs_def=to_addrs0,
                                                   to_addrs1_def=to_addrs1)
                if type(to_addrs0) is list:
                    check_send_bot = True
        else:
            if obj_time_start <= res_now or res_now <= obj_time_end:
                to_addrs0, msg_To = _check_filters(firma_filter_def=deepcopy(firma_filter),
                                                   firma_def=firma,
                                                   to_addrs_def=to_addrs0,
                                                   to_addrs1_def=to_addrs1)
                if type(to_addrs0) is list:
                    check_send_bot = True
    except ValueError as e:
        logging.info(f"Ошибка при преобразовании времени: {e}, который указан в файле email.ini")

    # create the message
    msg = MIMEMultipart()
    msg["From"] = e_mail
    msg["Sender"] = FROM
    msg["To"] = msg_To
    msg['Reply-To'] = e_mail
    msg["Subject"] = "Заявка из Телеграмм Бота"
    msg["Date"] = formatdate(localtime=True)

    html = get_html(e_mail, firma, full_name, cont_telefon, description, priority)

    if html:
        msg.attach(MIMEText(html, "html"))

    files_list = []
    if http_to_attach is not None and http_to_attach:
        for key_iter in http_to_attach.keys():
            path = f'documents/{http_to_attach[key_iter][0]}/{http_to_attach[key_iter][1]}'
            try:
                os.makedirs(path)
            except OSError:
                logging.info(f"Создать директорию %s не удалось: {path}")
            pahh_file = wget.download(key_iter,
                                      f'documents/{http_to_attach[key_iter][0]}/'
                                      f'{http_to_attach[key_iter][1]}/'
                                      f'{http_to_attach[key_iter][2]}')
            files_list.append(pahh_file)
        process_attachment(msg, files_list)
    try:
        server = smtplib.SMTP(host)
    except Exception as e:
        logging.info(f"Ошибка при создании сервера SMTP: {e}")
        val_error = 2
        return val_error
    try:
        server.starttls()
        server.login(FROM, password)
        server.sendmail(FROM, to_addrs0, msg.as_string())
    except Exception as e:
        logging.info(f"Ошибка при отправке письма: {e}")
        val_error = 3
    finally:
        server.quit()

    # удаляем временные файлы
    if len(files_list) != 0:
        str1 = str(files_list[0])
        path = str1[:str1.find('/', str1.find('/')+1)]
        shutil.rmtree(path, ignore_errors=False, onerror=None)

    return val_error, check_send_bot
    # ==========================================================================================================================



if __name__ == '__main__':
    send_email_with_attachment(e_mail='dffdvfd@fd.ru',
                                           firma="ООО kjhdk",
                                           full_name='Иван',
                                           cont_telefon='49834889',
                                           description='Ура!',
                                           priority="Низкий",
                                           message_id=1111111)

