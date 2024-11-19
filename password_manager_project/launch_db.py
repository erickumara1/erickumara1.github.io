import pg8000

def connect_db():
    try:
        db_name = "vault_db"
        db_user = "postgres"
        db_password = "docker"
        db_host = "localhost"
        db_port = 5432

        connection = pg8000.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        print("Connected to the PostgreSQL database.")

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT 1")  # Test query
            print("Cursor is open")
        except Exception as e:
            print("Cursor is closed or invalid:", e)

        return cursor

    except: 
        print('Connection to PostgreSQL Error')        
