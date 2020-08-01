This program works by running the test files test_host.py and test_client.py

To run:
python ./test_host.py

python ./test_client.py

The first host file is needed to be ran first to create the host server that will listen to any attempted connections on port 12371.
The client file can be ran after and will be receive a response on the options that the user is able to send back. (Signup / Login)

After signing up, the file /BlackJack/host/users.csv will be updated to show the new user with their chosen userID, salt value (64 bit), 
      and SHA256(salt+password) hex value

Imported Modules:
Cryptography library for RSA Encryption