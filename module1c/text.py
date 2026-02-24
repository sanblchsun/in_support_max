from datetime import datetime


def get_text(e_mail, firma, full_name, cont_telefon, description, priority):
    now_date = datetime.now()
    now_date = now_date.replace(second=0, microsecond=0)
    txt = f"""
Поступила из Телеграм БОТ новая заявка.

Автор оставил такие данные:

Компания: 	{firma}
Фамилия Имя: 	{full_name}
Контактный телефон: 	{cont_telefon}
E-mail адрес: 	{e_mail}
Описание проблемы: 	{description}
Приоритет заявки: 	{priority}


~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

Дата создания сообщения: {now_date}
"""
    return txt

