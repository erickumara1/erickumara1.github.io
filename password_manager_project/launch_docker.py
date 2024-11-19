import docker
import time
from launch_db import connect_db


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


    


    
