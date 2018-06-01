import asyncio
import struct

SERVER_COMMON_NAME = "test_server"

class ConnectionHandler(asyncio.Protocol):
  def __init__(self, connectivity_manager):
    self.connectivity_manager = connectivity_manager
    self.message = bytearray()
    self.message_length_remaining = 0

  def connection_made(self, transport):
    self.transport = transport
    # thanks to https://stuff.mit.edu/afs/sipb/project/snipe/snipe/lib/aiohttp/connector.py
    sock = self.transport._ssl_protocol._sslpipe.ssl_object
    server_cert = sock.getpeercert()
    common_name = server_cert["subject"][5][0][1]
    try:
      assert common_name == SERVER_COMMON_NAME
    except AssertionError:
      self.transport.close()
      raise Exception("Server Common Name ({}) does not match expected Common Name ({}).".format(common_name, SERVER_COMMON_NAME))
    self.connectivity_manager.set_connection_handler(self)

  def connection_lost(self, exc):
    self.connectivity_manager.connection_lost(exc)

  def data_received(self, data):
    if self.message_length_remaining > 0:
      assert len(data) <= self.message_length_remaining
      self.message = bytearray().join([self.message, data])
      self.message_length_remaining -= len(data)
    else:
      data_length = len(data) - 4
      message_length, message_bytes = struct.unpack("!I{}s".format(data_length), data)
      self.message = message_bytes
      assert data_length <= message_length
      self.message_length_remaining = message_length - data_length
    if self.message_length_remaining == 0:
      self.connectivity_manager.message_received(self.message)

  def send_message(self, message):
    data = struct.pack("!I{}s".format(len(message)), len(message), message)
    self.transport.write(data)

  def close(self):
    self.transport.close()