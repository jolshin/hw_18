import psycopg2

class DatabaseExecutor:

    def create_db(self):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
	        id SERIAL PRIMARY KEY,
	        f_name VARCHAR (40) NOT NULL,
	        l_name VARCHAR (40) NOT NULL,
	        email VARCHAR (80) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS phones (
	        id SERIAL PRIMARY KEY,
	        client_id INTEGER NOT NULL REFERENCES clients(id),
	        phone VARCHAR(20) NOT NULL
        );
        """)
        conn.commit()

    def add_client(self, f_name, l_name, email, status):
        table = ''

        if f_name != '' and l_name != '' and email != '':
            cur.execute("""
            INSERT INTO clients(f_name, l_name, email) VALUES(%s, %s, %s)
            """, (f_name, l_name, email))
            conn.commit()

            print('Запись внесена')

        elif status != '':
            print('Недостаточно данных для записи')

        cur.execute("""
        SELECT * FROM clients;
        """)

        table = cur.fetchall()

        for i in table:
            print(f'ID записи: {i[0]} \
                \nИмя клиента: {i[1]} \
                \nФамилия клиента: {i[2]} \
                \nemail: {i[3]}')
        
    def add_phone(self, client_id, phone, status):
        table = ''

        if client_id != '' and phone != '':
            cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES(%s, %s)
            """, (client_id, phone))
            conn.commit()

            print('Запись внесена')

        elif status != '':
            print('Недостаточно данных для записи')

        cur.execute("""
        SELECT * FROM phones;
        """)

        table = cur.fetchall()

        for i in table:
            print(f'ID записи: {i[0]} \
                \nID клиента: {i[1]} \
                \nНомер телефона: {i[2]}')
    
    def rec_update(self, id, f_name, l_name, email):

        if id != '' and f_name != '' and l_name != '' and email != '':
            cur.execute("""
            UPDATE clients SET f_name=%s, l_name=%s, email=%s WHERE id=%s;
            """, (f_name, l_name, email, id))
            conn.commit()

            print('Данные обновлены')

        else:
            print('Недостаточно данных для обновления записи')
        
        self.add_client('','','','')

    def del_phone(self, phone):

        if phone != '':
            cur.execute("""
            DELETE FROM phones WHERE phone=%s;
            """, (phone,))
            conn.commit()

            print('Данные удалены')
        
        else:
            print('Отсутствуют данные для удаления записи')

        self.add_phone('','','')

    def del_client(self, id):

        if id != '':
            cur.execute("""
            DELETE FROM clients WHERE id=%s;
            """, (id,))
            conn.commit()

            print('Данные удалены')
        
        else:
            print('Отсутствуют данные для удаления записи')

        self.add_client('','','','')

    def find_client(self, f_name, l_name, email, phone):
        
        id = ''
        query = ''

        if phone != '':
            cur.execute("""
            SELECT client_id FROM phones WHERE phone=%s;
            """, (phone,))

            id = cur.fetchone()

            cur.execute("""
            SELECT * FROM clients WHERE id=%s;
            """, (id,))

            query = cur.fetchone()
            
            if query is not None:
                print(f'ID клиента: {query[0]} \
                    \nИмя клиента: {query[1]} \
                    \nФамилия клиента: {query[2]} \
                    \nemail клиента: {query[3]}')
            else:
                print('Запись отсутсвтует')

        elif f_name != '' and l_name != '' and email != '':
            cur.execute("""
            SELECT * FROM clients WHERE f_name=%s AND l_name=%s AND email=%s;
            """, (f_name, l_name, email))

            query = cur.fetchone()
            
            if query is not None:
                print(f'ID клиента: {query[0]} \
                    \nИмя клиента: {query[1]} \
                    \nФамилия клиента: {query[2]} \
                    \nemail клиента: {query[3]}')
            else:
                print('Запись отсутсвтует')

        else:
            print('Отсутствуют данные для поиска')
            
            self.show()

    def drop_tables(self):

        cur.execute("""
        DROP TABLE phones;
        DROP TABLE clients;
        """)
        conn.commit()

        print('Записи в таблицах удалены')

    def show(self):
        self.add_client('','','','')
        self.add_phone('','','')

def helper():
    print('Перечень команд: \
            \nshow - показать данные таблиц \
            \ncr - создать структуру БД \
            \ndr - очистить таблицы БД (drop) \
            \nac - добавить запись о клиенте \
            \nap - добавить запись о телефоне клиента \
            \nru - изменить запись о клиенте \
            \ndp - удалить запись о телефоне клиента \
            \ndc - удалить запись о клиенте \
            \nfc - найти запись о клиенте \
            \nq - выход\n')

if __name__ == '__main__':


    
    with psycopg2.connect(database="hw_18", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            while True:
                result = DatabaseExecutor()

                comm = input('Команда:')

                if comm == 'cr':
                    result.create_db()
                elif comm == 'dr':
                    result.drop_tables()
                elif comm == 'ac':
                    result.add_client(input('Введите имя: '), input('Введите фамилию: '), input('Введите почту: '), 'input')
                elif comm == 'ap':
                    result.add_phone(input('Введите ID клиента: '), input('Введите телефон: '), 'input')
                elif comm == 'ru':
                    result.rec_update(input('Введите ID клиента, запись которого требуется обновить: '), \
                        input('Введите новое имя: '), input('Введите новую фамилию: '), input('Введите новый email: '))
                elif comm == 'dp':
                    result.del_phone(input('Введите номер телефона, который требуется удалить: '))
                elif comm == 'dc':
                    result.del_client(input('Введите ID клиента, данные о котором требуется удалить'))
                elif comm == 'fc':
                    result.find_client(input('Введите имя клиента: '), \
                        input('Введите фамилию клиента: '), input('Введите email клиента: '), \
                        input('Введите номер телефона клиента: '))
                elif comm == 'show':
                    result.show()
                elif comm == 'q':
                    break
                else:
                    helper()