from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
CHAT_ID = env.int("CHAT")  # Забираем значение типа int
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста


HOST=env.str("HOST")
PORT=env.int("PORT")
USER=env.str("USER")
PASSWORD=env.str("PASSWORD")
DATABASE=env.str("DATABASE")