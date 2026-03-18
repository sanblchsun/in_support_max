import html


def get_html(description=' ', priority=' '):

    description = html.escape(description)
    priority = html.escape(priority)
    description = html.escape(description.strip())

    html_text = f"""
<i><b>Описание проблемы:</b></i>
<code>{description}</code>
<i><b>Приоритет заявки:</b></i>
<code>{priority}</code>
"""
    return html_text