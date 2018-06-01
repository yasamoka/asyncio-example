import logging

class ConnectivityManager:
  def __init__(self, usernames, names, logging_level, fh, ch):
    self.logger = logging.getLogger('ConnectivityManager')
    self.logging_level = logging_level
    self.logger.setLevel(self.logging_level)
    self.logger.addHandler(fh)
    self.logger.addHandler(ch)
    self.logger.debug("Started")
    self.usernames = usernames
    self.names = names
    self.connected_clients = {}

  def client_connected(self, client_username, connection_handler):
    self.logger.info("Client connected: {} ({})".format(self.names[client_username], client_username))
    if client_username not in self.usernames:
      connection_handler.close()  # unknown clients are not allowed
      self.logger.warning("Unknown client {} - connection closed.".format(client_username))
    else:
      if client_username in self.connected_clients:
        self.connected_clients[client_username].close() # multiple connections from the same client are not allowed - close older connection
        self.logger.warning("Duplicate connection from client {} - older connection closed.".format(client_username))
      else:
        # do some small / asynchronous task here
        pass
      self.connected_clients[client_username] = connection_handler # add connection handler used for this client to dictionary of connected clients

  def client_disconnected(self, client_username, exc):
    self.connected_clients.pop(client_username)
    if exc is None:
      self.logger.info("Client disconnected: {}".format(client_username))
    else:
      self.logger.info("Client disconnected: {} - reason: \"{}\"".format(client_username, exc))

  def message_received(self, client_username, message):
    self.logger.debug("Received message from client {}: {}".format(client_username, message))
    # do some small / asynchronous task here
    # example: echo message
    self.connected_clients[client_username].send_message(message)