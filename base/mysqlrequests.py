# db.py

import asyncio
import aiomysql
from loguru import logger

pool = None


# -----------------------------
# ИНИЦИАЛИЗАЦИЯ ПУЛА
# -----------------------------
async def init_db(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
):

    global pool

    for attempt in range(5):  # 👈 retry при старте
        try:
            pool = await aiomysql.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                db=database,
                minsize=1,
                maxsize=5,
                autocommit=True,
            )

            logger.info("✅ Подключение к MySQL установлено")
            return

        except Exception as e:
            logger.error(f"❌ Ошибка подключения к БД (попытка {attempt+1}): {e}")
            await asyncio.sleep(2)

    raise RuntimeError("❌ Не удалось подключиться к MySQL")


# -----------------------------
# ЗАКРЫТИЕ ПУЛА
# -----------------------------
async def close_db():

    global pool

    if pool:
        pool.close()
        await pool.wait_closed()
        logger.info("🔌 Пул соединений закрыт")


# -----------------------------
# ВЫПОЛНЕНИЕ ЗАПРОСА (универсально)
# -----------------------------
async def execute(query, args=None, fetchone=False, fetchall=False):

    global pool

    for attempt in range(3):  # 👈 retry при падении соединения
        try:
            async with pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:

                    await cursor.execute(query, args or ())

                    if fetchone:
                        return await cursor.fetchone()

                    if fetchall:
                        return await cursor.fetchall()

                    return None

        except Exception as e:
            logger.error(f"DB error (attempt {attempt+1}): {e}")
            await asyncio.sleep(1)

    raise RuntimeError("❌ Ошибка выполнения SQL после retry")


# -----------------------------
# ВСТАВКА ЗАЯВКИ
# -----------------------------
async def insert_request_to_mysql(
    e_mail,
    firma,
    full_name,
    cont_telefon,
    description,
    priority,
    message_id,
):

    # 1. получаем / создаём пользователя
    user = await execute(
        "SELECT id FROM users WHERE id_telegram=%s",
        (message_id,),
        fetchone=True,
    )

    if not user:
        await execute(
            "INSERT INTO users (id_telegram) VALUES (%s)",
            (message_id,),
        )

        user = await execute(
            "SELECT id FROM users WHERE id_telegram=%s",
            (message_id,),
            fetchone=True,
        )

    user_id = user["id"] # type: ignore

    # 2. создаём заявку
    await execute(
        """
        INSERT INTO requests 
        (user_id, full_name, firma, e_mail, telefon, description, priority, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """,
        (
            user_id,
            full_name,
            firma,
            e_mail,
            cont_telefon,
            description,
            priority,
        ),
    )

    logger.info(f"✅ Заявка записана в БД для пользователя {message_id}")