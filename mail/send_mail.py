import logging
import os
import smtplib
import sys
from configparser import ConfigParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from mail.html import get_html
import requests
from email.mime.base import MIMEBase
from email import encoders
from urllib.parse import urlparse




# ----------------------------------------------------------------------
def send_email_with_attachment(e_mail,
                                     firma,
                                     full_name,
                                     cont_telefon,
                                     description,
                                     priority,
                                     user_id,
                                     http_to_attach=None,
                                     ):
    """
    Send an email with an attachment
    """
    val_error = 0
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

    # create the message
    msg = MIMEMultipart()
    msg["From"] = e_mail
    msg["Sender"] = FROM
    msg["To"] = msg_To
    msg['Reply-To'] = e_mail
    msg["Subject"] = "Заявка из MAX Бота"
    msg["Date"] = formatdate(localtime=True)

    html = get_html(e_mail, firma, full_name, cont_telefon, description, priority)

    if html:
        msg.attach(MIMEText(html, "html"))
    else: 
        logging.error("Ошибка отправки почты")
        return 4
        # ---------- ATTACHMENTS ----------
    if http_to_attach:
        for key_iter in http_to_attach.keys():
            try:
                response = requests.get(http_to_attach[key_iter], timeout=10)
                response.raise_for_status()

                file_data = response.content

                # имя файла из URL
                parsed = urlparse(http_to_attach[key_iter])
                filename = key_iter

                part = MIMEBase("application", "octet-stream")
                part.set_payload(file_data)
                encoders.encode_base64(part)

                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{filename}"'
                )

                msg.attach(part)

            except Exception as e:
                logging.error(f"Ошибка при загрузке файла {http_to_attach[key_iter]}: {e}")
                val_error = 5    
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

    return val_error


