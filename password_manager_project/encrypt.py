from Crypto.Cipher import AES 
from hashlib import sha256
from pbkdf2 import PBKDF2
import string 
import secrets

def generate_random(length=20):
    option = string.ascii_lowercase + string.ascii_uppercase + string.digits
    random = ''.join([secrets.choice(option) for i in range(length)])
    return random

def find_hash(first_key, second_key=""):
    first_key = first_key.encode()
    second_key = second_key.encode()
    return sha256(first_key + second_key).hexdigest()

first_key = "Master1"
second_key = "Master2"

master_hash = find_hash(first_key,second_key)
print("master hash is ", master_hash)

master_salt = "MasterSalt"

password_salt = generate_random() + ":" + generate_random()
print("password generated is ", password_salt)

key = PBKDF2(master_hash,master_salt).read(32)
print(key)

entry = password_salt.encode()
cipher = AES.new(key, AES.MODE_EAX)
cipher_text, signature = cipher.encrypt_and_digest(entry)
print(cipher_text)

cipher2 = AES.new(key, AES.MODE_EAX, cipher.nonce)
plain_text = cipher2.decrypt_and_verify(cipher_text, signature)
print(plain_text.decode())
