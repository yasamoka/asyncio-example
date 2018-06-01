import asyncio
import ssl
import argparse
import json
import logging

from connection_handler import ConnectionHandler
from connectivity_manager import ConnectivityManager

LOGFILE = "server.log"
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

parser = argparse.ArgumentParser()
parser.add_argument("-ca", help="CA filepath", required=True)
parser.add_argument("-key", help="Key filepath", required=True)
parser.add_argument("-cert", help="Certificate filepath", required=True)
parser.add_argument("-host", help="Host", default="localhost")
parser.add_argument("-port", help="Port", required=True)
parser.add_argument("-accounts", help="Accounts JSON filepath", required=True)
args = parser.parse_args()

ca_filepath = args.ca
key_filepath = args.key
cert_filepath = args.cert
server_host = args.host
server_port = args.port
accounts_json_filepath = args.accounts

logger = logging.getLogger('Server')
logger.setLevel(LOGGING_LEVEL)
fh = logging.FileHandler(LOGFILE)
fh.setLevel(LOGGING_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter(LOGGING_FORMAT)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

with open(accounts_json_filepath) as accounts_json_file:
  accounts_json = json.load(accounts_json_file)

usernames = [None] * len(accounts_json)
names = {}
for i in range(len(accounts_json)):
  account_json = accounts_json[i]
  usernames[i] = username = account_json["username"]
  names[username] = account_json["name"]

loop = asyncio.get_event_loop()
connectivity_manager = ConnectivityManager(usernames, names, LOGGING_LEVEL, fh, ch)
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=ca_filepath)
ssl_context.load_cert_chain(cert_filepath, key_filepath)
ssl_context.verify_mode = ssl.CERT_REQUIRED
server_coro = loop.create_server(lambda: ConnectionHandler(connectivity_manager), server_host, server_port, ssl=ssl_context)
server = loop.run_until_complete(server_coro)
loop.run_forever()