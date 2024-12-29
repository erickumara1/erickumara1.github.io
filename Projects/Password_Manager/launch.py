import docker
import time
import pg8000

def start_docker(image_name, container_name, client):
    try:
        if image_name not in str(client.images.list(all=True)): 
            client.images.build(path='./',tag=image_name)
            print('Vault Database Image has been created')
        else:
            print('Vault Database Image already created')
    except:
        print('Vault Database Image Creation Error')
 
    try:
        if len(client.containers.list(all=True, filters={'ancestor': image_name})) == 0:
            print('Vault Database Container has been created')
            container = client.containers.create(
                                image=image_name, 
                                name=container_name,
                                ports={'5432/tcp': 5432})
        else:
            print('Vault Container already created')
            container = client.containers.get(container_name)
    except:
        print('Vault Database Container Creation Error')

    return container

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

        return connection

    except: 
        print('Connection to PostgreSQL Error')        

if __name__ == "__main__":

    #EDIT NAME 
    image_name = 'vault_db_image'
    container_name = 'vault_db_container'

    # starting image and container 
    client = docker.from_env()
    container = start_docker(image_name,container_name, client)
    container.start()

    # connection to database and cursor
    print("Waiting for Container to Boot")
    time.sleep(3)
    cursor = connect_db()    
 