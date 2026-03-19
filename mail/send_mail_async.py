import asyncio
import logging
import mimetypes
import os
import shutil
import sys
from configparser import ConfigParser
from copy import deepcopy
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from mail.html import get_html
import aiofiles
import aiohttp
from datetime import datetime, time
import aiosmtplib


def _check_filters(firma_filter_def, firma_def, to_addrs_def, to_addrs1_def):
    if firma_filter_def:
        firma_filter_def = [i.strip() for i in firma_filter_def.split(",")]
        if len(firma_filter_def) <= 100:
            for i_pattern in firma_filter_def:
                if i_pattern.lower() in firma_def.lower():
                    return [
                        to_addrs_def,
                        to_addrs1_def,
                    ], f"{to_addrs_def}; {to_addrs1_def}"
        else:
            logging.info("в файле email.ini возможно строка firma_filter = пустая")
    return to_addrs_def, f"{to_addrs_def}"


async def async_download_file(url: str, dest_path: str):
    """Асинхронная загрузка файла."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(dest_path, "wb") as f:
                    await f.write(await resp.read())
                return dest_path
            else:
                logging.error(f"Ошибка загрузки {url}: {resp.status}")
                return None


async def send_email_with_attachment(
    e_mail,
    firma,
    full_name,
    cont_telefon,
    description,
    priority,
    message_id,
    http_to_attach=None,
    number_from_1c="",
):
    """Асинхронная отправка письма с вложениями."""
    val_error = 0
    check_send_bot = False
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")

    if not os.path.exists(config_path):
        print("Config not found! Exiting!")
        sys.exit(1)

    cfg = ConfigParser()
    cfg.read(config_path)

    host = cfg.get("smtp", "server")
    FROM = cfg.get("smtp", "from")
    PORT = int(cfg.get("smtp", "port"))
    password = cfg.get("smtp", "passwd")
    to_addrs = cfg.get("smtp", "to_addrs")
    to_addrs1 = cfg.get("smtp", "to_addrs1")
    time_start = cfg.get("time", "time_start")
    time_end = cfg.get("time", "time_end")
    firma_filter = cfg.get("filter", "firma_filter")

    if not to_addrs:
        logging.info("Не указан основной адрес получателей в email.ini")
        return 1, False

    to_addrs0 = to_addrs
    msg_To = f"{to_addrs}"

    try:
        obj_time_start = time.fromisoformat(time_start)
        obj_time_end = time.fromisoformat(time_end)
        now = datetime.now().time()
        if obj_time_start <= obj_time_end:
            if obj_time_start <= now <= obj_time_end:
                to_addrs0, msg_To = _check_filters(
                    firma_filter, firma, to_addrs0, to_addrs1
                )
                if isinstance(to_addrs0, list):
                    check_send_bot = True
        else:
            if obj_time_start <= now or now <= obj_time_end:
                to_addrs0, msg_To = _check_filters(
                    firma_filter, firma, to_addrs0, to_addrs1
                )
                if isinstance(to_addrs0, list):
                    check_send_bot = True
    except ValueError as e:
        logging.info(f"Ошибка при обработке времени: {e}")

    # Формирование MIME-сообщения
    msg = MIMEMultipart()
    msg["From"] = e_mail
    msg["Sender"] = FROM
    msg["To"] = msg_To
    msg["Reply-To"] = e_mail
    msg["Subject"] = "Заявка из MAX Бота"
    msg["Date"] = formatdate(localtime=True)

    html = get_html(e_mail, firma, full_name, cont_telefon, description, priority)
    msg.attach(MIMEText(html, "html", "utf-8"))

    # Загрузка вложений (асинхронно)
    files_list = []
    if http_to_attach:
        for key, info in http_to_attach.items():
            path = f"documents/{info[0]}/{info[1]}/{info[2]}"
            downloaded = await async_download_file(key, path)
            if downloaded:
                files_list.append(downloaded)

    process_attachment(msg, files_list)

    # Отправка письма (асинхронно)
    try:
        smtp = aiosmtplib.SMTP(hostname=host, port=PORT, start_tls=True, timeout=150)
        await smtp.connect()
        await smtp.login(FROM, password)
        await smtp.send_message(msg, sender=FROM, recipients=to_addrs0, timeout=150)
        await smtp.quit()
    except aiosmtplib.errors.SMTPResponseException as e:
        logging.error(f"SMTP ошибка: {e.code} {e.message}")
        val_error = 3
    except aiosmtplib.errors.SMTPException as e:
        logging.error(f"Ошибка SMTP: {e}")
        val_error = 3
    except Exception as e:
        logging.exception(f"Ошибка при отправке письма: {e}")
        val_error = 3
    if len(files_list) != 0:
        str1 = str(files_list[0])
        path = str1[: str1.find("/", str1.find("/") + 1)]
        shutil.rmtree(path, ignore_errors=False, onerror=None)
    return val_error, check_send_bot


def process_attachment(msg, files):
    """Добавление вложений."""
    for f in files:
        if os.path.isfile(f):
            attach_file(msg, f)
        elif os.path.isdir(f):
            for file in os.listdir(f):
                attach_file(msg, os.path.join(f, file))


def attach_file(msg, filepath):
    """Добавление одного файла к письму."""
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"
    maintype, subtype = ctype.split("/", 1)

    with open(filepath, "rb") as fp:
        part = MIMEBase(maintype, subtype)
        part.set_payload(fp.read())
        encoders.encode_base64(part)

    part.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(part)


if __name__ == "__main__":
    asyncio.run(
        send_email_with_attachment(
            e_mail="test@test.ru",
            firma="ООО Ромашка",
            full_name="Иван Иванов",
            cont_telefon="89998887766",
            description="Проверка асинхронной отправки",
            priority="Низкий",
            message_id=12345,
        )
    )
