import asyncio
import sys
import time
from brom import *
from configparser import ConfigParser
from module1c.text import get_text


@staticmethod
def connect1c():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "settings.ini")

    # get the config
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)

    url_to_base = cfg.get("connect", "urlToBase")
    login = cfg.get("connect", "login")
    passwd = cfg.get("connect", "passwd")
    # Проверка на путь к базе
    try:
        klient = БромКлиент(
            f"{url_to_base}", f"{login}", f"{passwd}"
        )
    except Exception as e:
        print(e)
        klient = False
    # Проверка логина и пароля
    try:
        klient.ПолучитьИнформациюОСистеме()
    except Exception as e:
        klient = False

    return klient


async def get_where_number(num, count=500):
    klient = connect1c()
    if not klient:
        return False

    textRequest = klient.СоздатьЗапрос(f"""
            ВЫБРАТЬ ПЕРВЫЕ {count}
                Инцидент.Дата КАК Дата,
                Инцидент.Состояние.Наименование КАК СостояниеНаименование,
                Инцидент.Описание КАК Описание,
                Инцидент.Номер КАК Номер
            ИЗ
                Документ.Инцидент КАК Инцидент

            ГДЕ Инцидент.Номер = "{num}"
        """)

    res = textRequest.Выполнить()

    for item in res:
        print(f"""
Дата:
    {item.Дата}
Номер:
    {item.Номер}
Состояние:
    {item.СостояниеНаименование}
Описание:
    {item.Описание}""")
    print("==========================================================================")


async def get_status(num):
    klient = connect1c()
    if not klient:
        return False

    textRequest = klient.СоздатьЗапрос(f"""
            ВЫБРАТЬ
                Инцидент.Состояние.Наименование КАК СостояниеНаименование
            ИЗ
                Документ.Инцидент КАК Инцидент

            ГДЕ Инцидент.Номер = "{num}"
        """)

    res = textRequest.Выполнить()
    res_str = res[0].СостояниеНаименование
    if type(res_str) is not str:
        res_str = "Статус не присвоен"
    return res_str


async def get_count(count=500):
    klient = connect1c()
    if not klient:
        return False

    textRequest = klient.СоздатьЗапрос(f"""
            ВЫБРАТЬ ПЕРВЫЕ {count}
                Инцидент.Дата КАК Дата,
                Инцидент.Состояние.Наименование КАК СостояниеНаименование,
                Инцидент.Описание КАК Описание,
                Инцидент.Номер КАК Номер
            ИЗ
                Документ.Инцидент КАК Инцидент

            УПОРЯДОЧИТЬ ПО
                Дата УБЫВ
        """)

    res = textRequest.Выполнить()

    for item in res:
        print(f"""
Дата:
    {item.Дата}
Номер:
    {item.Номер}
Состояние:
    {item.СостояниеНаименование}
Описание:
    {item.Описание}""")
        print("==========================================================================")


async def set_brom(e_mail, firma, full_name, cont_telefon, description, priority):
    klient = connect1c()
    if not klient:
        return "Заявке номер не присвоен"

    docObject = klient.Документы.Инцидент.СоздатьДокумент()
    request_text = klient.СоздатьЗапрос("""
ВЫБРАТЬ
	Клиенты.Наименование КАК Наименование
ИЗ
	Справочник.Клиенты КАК Клиенты
ГДЕ
	Клиенты.Наименование ПОДОБНО &firma
""")
    request_text.УстановитьПараметр("firma", f"%{firma}%")
    res = request_text.Выполнить()
    if len(res) == 0:
        firma_1c = firma
    else:
        firma_1c = res[0].Наименование

    # Заполняем реквизиты
    docObject.Дата = datetime.today()
    docObject.ТемаОбращения = "Новая заявка"
    docObject.Клиент = klient.Справочники.Клиенты.НайтиПоНаименованию(firma_1c)
    # docObject.Приоритет = klient.Справочники.Приоритеты.НайтиПоНаименованию("Низкий")
    docObject.Описание = get_text(e_mail=e_mail,
                                  firma=firma,
                                  full_name=full_name,
                                  cont_telefon=cont_telefon,
                                  description=description,
                                  priority=priority)
    docObject.Состояние = klient.Справочники.СостоянияИнцидентов.НайтиПоНаименованию("00. Новая заявка")

    # докОбъект.КонтактноеЛицо   = клиент.Справочники.Пользователи.НайтиПоНаименованию("Александрова Алена")
    # докОбъект.Ответственный    = клиент.Справочники.Сотрудники.НайтиПоНаименованию("Макосов Александр Александрович")
    # докОбъект.Услуга           = клиент.Справочники.Услуги.НайтиПоНаименованию("01. Рабочие места пользователей")
    # докОбъект.КомпонентаУслуги = клиент.Справочники.СоставУслуг.НайтиПоНаименованию("01.01 Установка и настройка ЭЦП")
    # докОбъект.Тип              = клиент.Справочники.ИТ_ТипыИнцидентов.НайтиПоНаименованию("Запрос на обслуживание")

    # Записываем состояние объекта в режиме проведения
    docObject.Записать()
    # Получаем ссылку на созданный документ
    docLink = docObject.Ссылка
    return docLink.Номер


# if __name__ == "__main__":
#     start = time.time()
#     # asyncio.run(set_brom("dashjkjh", "Буревестник (АГ Марин)"))
#     asyncio.run(set_brom(e_mail="test@test.ru",
#                          firma="Марин",
#                          full_name="Test Testovich",
#                          cont_telefon="9991111111",
#                          description="TEST",
#                          priority="низкий"))
#     end = time.time()
#     print("The time of execution of above program is :",
#           (end - start) * 10 ** 3, "ms")
