import asyncio
import struct
import logging

CMD_EXIT = "exit"

class ConnectivityManager:
  def __init__(self, logging_level, fh, ch):
    self.logger = logging.getLogger('ConnectivityManager')
    self.logging_level = logging_level
    self.logger.setLevel(self.logging_level)
    self.logger.addHandler(fh)
    self.logger.addHandler(ch)
    self.logger.debug("Started")

  def set_connection_handler(self, connection_handler):
    self.connection_handler = connection_handler
    self.logger.info("Connected to server.")
    print()
    self.user_input()

  def connection_lost(self, exc):
    if exc is None:
      self.logger.info("Connection lost.")
    else:
      self.logger.info("Connection lost - reason: {}".format(exc))
    self.shutdown()

  def shutdown(self):
    self.logger.debug("Cancelling all tasks ...")
    for task in asyncio.Task.all_tasks():
      self.logger.debug("Canceling task: {}".format(task))
      task.cancel()
    self.logger.debug("Closing connection handler ...")
    self.connection_handler.close()

  def message_received(self, message):
    self.logger.debug("Received message from server: {}".format(message))
    # parse message here

    # do some task here - asynchronous if you still expect to receive messages from server and process them in the meantime
    # example: print echoed message and get user input
    print("\nServer response: {}".format(message))
    self.user_input()

  def user_input(self):
    while True:
      cmd = input("> ")
      if cmd == "":
        continue
      if cmd.lower() == CMD_EXIT:
        self.shutdown()
        return
      message = cmd.encode('utf-8')
      self.connection_handler.send_message(message)
      break