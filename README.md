# Black Jack
## Network Security Project FPU SP 2020
## Produced by Jeremy Wade & Tito Leadon

Project is now over and no longer supported; was severely cripped in productivity during COVID 19
May come back later to fix problems, improve design (Major Refactor, Implement user database rather than .txt files for users, add AES Encryption)

## Goal
The goal of this project is to not create a fully developing BlackJack App but instead to utilize different 
security measures that could be implemented for both in house and users. It is NOT advised to use any part
of the code that was produced in a deployed project.

Originally, the project was to create all encryption and decryption modules from scratch. Due to time constraints imposed by COVID-19 and
problems that had been presented (Both contributors being forced to move), this was abandoned. 

## Security Implementations
The security features adopted include:
  RSA Encryption (2048 bit) for secure communication through a network (Prevents Man in Middle)
  
  Salting (64 bit) & HASH (SHA 256) new user passwords (Prevents Inside Intrusion from viewing passwords & Rainbow attack)
  
  Prevention of inputting common passwords (Looks through list of 10,000 of most commonly used passwords) (Help Prevent Brute Force)
  
  Requires at least 12 character passwords (Help Prevent Brute Force)
  
  Attempted Login Limit of 3 (Help Prevent Brute Force)
  
  Blacklist of IP after too many failed Login Attempts (Help Prevent Brute Force)
  
## Problems
Known problems in the program:
  No current protection from Replay Attacks
  
    -> Future iterations may include Nonce / Timestamp attached to each message to accept / deny messages
    
  The Random Number Generator for producing keys is not totally random; used standard library Random module 
  
    -> Can pull Random numbers from random.org API. This uses radio receivers from where they are located to pickup
       atmospherioc noise for entropy opposed to using the current system time on the running machine.
       
  Does not send two cards to both host and user, was not a concern as the scope was not meant to be a fully developed game but rather
  utilizing what was learned in Network Security.

## How to Run
This program works by running the test files test_host.py and test_client.py
Client.py & Host.py showcase the order of operations needed and Encryption/Decryption needed with what key

To run host:
python ./test_host.py

to run client:
python ./test_client.py

The first host file is needed to be ran first to create the host server that will listen to any attempted connections on port 12371.
The client file can be ran after and will be receive a response on the options that the user is able to send back. (Signup / Login)

After signing up, the file /BlackJack/host/users.csv will be updated to show the new user with their chosen userID, salt value (64 bit), 
      and SHA256(salt+password) hex value

## Dependencies
Imported Modules:
Cryptography library for RSA Encryption
