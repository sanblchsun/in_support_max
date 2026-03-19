import datetime
from loguru import logger
import os
import sys
from configparser import ConfigParser
import aiomysql


async def write_to_mysql(
    e_mail: str,
    firma: str,
    full_name: str,
    cont_telefon: str,
    description: str,
    priority: str,
    message_id: int,
):
    """Асинхронная запись данных в MySQL"""

    # Получаем настройки подключения из mysql.ini
    global conn
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "mysql.ini")

    if not os.path.exists(config_path):
        logger.error("❌ Файл mysql.ini не найден")
        sys.exit(1)

    cfg = ConfigParser()
    cfg.read(config_path)

    host = cfg.get("connect", "host")
    port = int(cfg.get("connect", "port"))
    user = cfg.get("connect", "user")
    password = cfg.get("connect", "password")
    database = cfg.get("connect", "database")

    # Подключение к БД
    try:
        conn = await aiomysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=False,
        )

        async with conn.cursor(aiomysql.DictCursor) as cursor:
            # Проверяем наличие пользователя
            await cursor.execute(
                "SELECT id FROM users WHERE id_telegram=%s", (message_id,)
            )
            rows = await cursor.fetchall()

            if not rows:
                await cursor.execute(
                    "INSERT INTO users (id_telegram) VALUES (%s)", (message_id,)
                )
                await cursor.execute(
                    "SELECT id FROM users WHERE id_telegram=%s", (message_id,)
                )
                rows = await cursor.fetchall()

            user_id = rows[0]["id"]

            # Добавляем заявку
            sql_requests = """
                INSERT INTO requests 
                    (user_id, full_name, firma, e_mail, telefon, description, priority, date)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            await cursor.execute(
                sql_requests,
                (
                    user_id,
                    full_name,
                    firma,
                    e_mail,
                    cont_telefon,
                    description,
                    priority,
                    datetime.datetime.now(),
                ),
            )

            await conn.commit()
            logger.info(
                f"✅ Заявка успешно добавлена  в базу для пользователя {message_id}"
            )

    except Exception as e:
        logger.error(f"❌ Ошибка при работе с базой данных MySQL {e}")
    finally:
        if "conn" in locals():
            await conn.close()
