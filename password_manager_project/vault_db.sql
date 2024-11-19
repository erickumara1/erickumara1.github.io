--the database will have 3 columns, URL, Username, Password
-- the values will be hashed with salting using SHA-256
-- the master key of the PM is the initialization vector for SHA-256
-- output is 256 bits = 32 bytes = 64 charachter, 1 bytes = 2 charachter

CREATE TABLE vault_table
(
    url VARCHAR(64) NOT NULL,
    username VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL
);

--initializing testing values to see if docker can launch vault_table
INSERT INTO vault_table
VALUES('test_url','test_username','test_password');