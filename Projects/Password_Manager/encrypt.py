from Crypto.Cipher import AES 
from hashlib import sha256
from pbkdf2 import PBKDF2

import launch
import base64
import string 
import secrets

def generate_random(length=20):
    option = string.ascii_lowercase + string.ascii_uppercase + string.digits
    random = ''.join([secrets.choice(option) for i in range(length)])
    return random

def add_salt(p):
    return p + ":" + generate_random()

def find_hash(first_key, second_key=""):
    first_key = first_key.encode()
    second_key = second_key.encode()
    return sha256(first_key + second_key).hexdigest()

def encrypt(key,p):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce =  base64.b64encode(cipher.nonce)

    p = p.encode('utf-8')
    c = cipher.encrypt(p)
    c = base64.b64encode(c)

    return c, nonce

def decrypt(key, nonce, c):
    c = base64.b64decode(c)
    nonce = base64.b64decode(nonce)

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    p = cipher.decrypt(c)
    return p

############### 
#TESTING 
#Adding Data to Table
######################

url = input("url:")
url = add_salt(url)

username = input("username:")
username = add_salt(username)

password = add_salt(generate_random())

first_key = "Master1"
second_key = "Master2"
master_hash = find_hash(first_key,second_key)

master_salt = "MasterSalt"
key = PBKDF2(master_hash,master_salt).read(32)

url_cipher, url_nonce = encrypt(key,url)
print("url encrypted", url_cipher, url_nonce)

user_cipher, user_nonce = encrypt(key,username)
print("url encrypted", user_cipher, user_nonce)

pass_cipher, pass_nonce = encrypt(key,password)
print("url encrypted", pass_cipher, pass_nonce)

url_plain = decrypt(key,url_nonce, url_cipher)
print("url decrypted ", url_plain)

print("url_nonce length:", len(url_nonce))
print("url_cipher length:", len(url_cipher))
print("user_cipher length:", len(user_cipher))
print("user_nonce length:", len(user_nonce))
print("pass_cipher length:", len(pass_cipher))
print("pass_nonce length:", len(pass_nonce))

connection = launch.connect_db()
cursor = connection.cursor()

cursor.execute('''INSERT INTO vault_table
VALUES (%s, %s, %s, %s, %s, %s);''',
(url_nonce, url_cipher, user_cipher, user_nonce, pass_cipher, pass_nonce))
connection.commit()

cursor.execute('''SELECT * FROM vault_table''')
rows = cursor.fetchall()
for row in rows:
    print(row)

if len(rows) >=3 :
    cursor.execute('''DELETE FROM vault_table''')
    connection.commit()


# cipher_text = base64.b64decode(p_cipher)
# cipher2 = AES.new(key, AES.MODE_EAX, nonce)
# plain_text = cipher2.decrypt(cipher_text)

# print("password decrypted", plain_text.decode())
