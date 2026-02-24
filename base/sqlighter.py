# telegram_id|full_name|firma|e_mail|telefon

import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # def get_subscriptions(self, status = True):
    #     """Получаем всех активных подписчиков бота"""
    #     with self.connection:
    #         return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def get_client(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `clients` WHERE `telegram_id` = ?', (user_id,)).fetchall()
            return result

    def get_admins_firms(self, usr_id):
        with self.connection:
            result = self.cursor.execute(f"SELECT firma FROM admin WHERE tlgrm_id_adm = {usr_id}").fetchall()
            return result

    def del_subscriptions_for_admin(self,usr_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM admin WHERE `tlgrm_id_adm` == ?", (usr_id,))



    def update_admin(self, user_id, firma):
        """Обновляем подписчика"""
        with self.connection:
            return self.cursor.execute("UPDATE `admin` SET `firma` = ? WHERE `tlgrm_id_adm` = ?", (firma, user_id))

    def add_admin(self, user_id, list_firms):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'admin' ('tlgrm_id_adm', 'full_name', 'firma', 'e_mail', 'telefon') VALUES(?,?,?,?,?)",
                                       (int(user_id), None, str(list_firms), None, None))

    def add_user(self, user_id, full_name, telephon, e_mail, firma):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'clients' ('telegram_id', 'full_name', 'firma', 'e_mail', 'telefon') VALUES(?,?,?,?,?)",
                                       (int(user_id), str(full_name), str(firma), str(e_mail), str(telephon)))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def delete_user_data(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM clients WHERE telegram_id == ?", (user_id,))

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


# if __name__ == '__main__':
#     sql_object = SQLighter('db.db')
# """в скобках указать из телеграмм ID админа"""
#     res = sql_object.get_admins_firms()
#     res1 = res[0][0].split(",")
#     print(res1)
#     for i in res1:
#         print(i.lower().strip())
