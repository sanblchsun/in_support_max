from datetime import datetime


def get_html(e_mail, firma, full_name, cont_telefon, description, priority, number_from_1c=''):
    now_date = datetime.now()
    now_date = now_date.replace(second=0, microsecond=0)
    html = f"""
<html>
<body>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<p> Поступила из Телеграмм БОТ новая заявка</p>
<p> Автор оставил такие данные:</p>
<p>
<table style="width: 100%; background: #ffffff; border: 1px
              solid #dddddd; border-collapse: collapse;" cellspacing="0" cellpadding="0" border="0">
    <tbody>
    <tr>
        <th style="width: 40%; padding: 7px; border: 1px solid
                    #dddddd; text-align: left;">Компания:
        </th>
        <td style="padding: 7px; border: 1px solid #dddddd;
                    text-align: left;">{firma}
        </td>
    </tr>
    <tr>
        <th style="width: 40%; padding: 7px; border: 1px solid
                    #dddddd; text-align: left;background: #f9f9f9;">Фамилия Имя:
        </th>
        <td style="padding: 7px; border: 1px solid #dddddd;
                    text-align: left;background: #f9f9f9;">{full_name}
        </td>
    </tr>
    <tr>
        <th style="width: 40%; padding: 7px; border: 1px solid
                    #dddddd; text-align: left;background: #f9f9f9;">Контактный телефон:
        </th>
        <td style="padding: 7px; border: 1px solid #dddddd;
                    text-align: left;background: #f9f9f9;">{cont_telefon}
        </td>
    </tr>
    <tr>
        <th style="width: 40%; padding: 7px; border: 1px solid
                    #dddddd; text-align: left;">E-mail адрес:
        </th>
        <td style="padding: 7px; border: 1px solid #dddddd;
                    text-align: left;">{e_mail}
        </td>
    </tr>
    <tr>
        <th style="width: 40%; padding: 7px; border: 1px solid
                    #dddddd; text-align: left;background: #f9f9f9;">Описание
            проблемы:
        </th>
        <td style="padding: 7px; border: 1px solid #dddddd;
                    text-align: left;background: #f9f9f9;">{description}
        </td>
    </tr>
    <tr>
        <th style="width: 40%; padding: 7px; border: 1px solid
                    #dddddd; text-align: left;background: #f9f9f9;">
            Приоритет заявки:
        </th>
        <td style="padding: 7px; border: 1px solid #dddddd;
                    text-align: left;background: #f9f9f9;">{priority}
        </td>
    </tr>

    </tbody>
</table>
<br>
~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-<br>
<br>
Дата создания сообщения: {now_date}
</p>
</body>
</html>
"""
    return html

