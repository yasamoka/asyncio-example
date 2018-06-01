Tested with Python 3.6.5 on Windows 10 April Update and Ubuntu 18.04.

Uses the following libraries:

asyncio: https://docs.python.org/3/library/asyncio.html  
ssl: https://docs.python.org/3/library/ssl.html  
argparse: https://docs.python.org/3/library/argparse.html  
json: https://docs.python.org/3/library/json.html  
logging: https://docs.python.org/3/library/logging.html

To generate the CA, server, and client keys and certificates, run the generate-keys.bat (Windows) or generate-keys.sh (macOS / Linux) file.

You will need to generate the keys and certificates for SSL server & client authentication to work.

To run the server, run the run-server.bat (Windows) or run-server.sh (macOS / Linux) file inside the folder "server".

To run the client, run the run-client.bat (Windows) or run-client.sh (macOS / Linux) file inside the folder "client".