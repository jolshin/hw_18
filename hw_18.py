import psycopg2

class DatabaseExecutor:
    
    def __init__(self, databse, user, password):
        self.query = query
        self.databse = database
        self.user = user
        self.password = password

    def create_db(self):
        cur.execute("""
        CREATE TABLE IF NOTT EXISTS clients (
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

    def add_cleint(self, id, f_name, l_name, email):
        cur.execute("""
        INSERT INTO clients VALUES(id, f_name, l_name, email)
        """)
        print('fetchone', cur.fetchone())
        

    def add_phone(self, id, client_id, phone):
        cur.execute("""
        INSERT INTO phones VALUES(id, client_id, phone)
        """)
        print('fetchone', cur.fetchone())
        
    
    def rec_update(self):
        pass

    def del_phone(self):
        pass

    def del_client(self):
        pass

    def find_client(self):
        pass

    def excutor(self, comm):
        pass

if __name__ == '__main__':
    
    with psycopg2.connect(database="hw_18", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:

            result = DatabaseExecutor(input('Что делаем?'))
            print(result)




