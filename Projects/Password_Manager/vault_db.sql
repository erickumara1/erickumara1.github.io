--the database will have 3 columns, URL, Username, Password
-- the values will be hashed with salting using AES-256
-- the master key of the PM a predetermined value punched out
-- output is 256 bits = 32 bytes = 64 charachter, 1 bytes = 2 charachter

CREATE TABLE vault_table
(
    url_nonce TEXT NOT NULL,
    url TEXT NOT NULL,
    username_nonce TEXT NOT NULL,
    username TEXT NOT NULL,
    password_nonce TEXT NOT NULL,
    password TEXT NOT NULL   
);

