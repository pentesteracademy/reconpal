from websocket_server import WebsocketServer
import subprocess
import datetime


def shell(cmd, client, server):
    """Called to execute shell commands received from controller module"""
    process = subprocess.Popen(
        [cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    current_time = datetime.datetime.now()
    while True:
        output = process.stdout.readline()
        if output is not None:
            output = output.rstrip().decode("utf-8", "ignore")
        if output == "" and process.poll() is not None:
            server.send_message(client, "--END--")
            break
        if output != "":
            server.send_message(client, output)
        if current_time < datetime.datetime.now() - datetime.timedelta(
            minutes=2
        ):
            server.send_message(client, "--END--")
            break


def new_client(client, server):
    """Called for every client connecting (after handshake)"""
    print("New client connected and was given id %d" % client["id"])


def client_left(client, server):
    """Called for every client disconnecting"""
    print("Client(%d) disconnected" % client["id"])


def message_received(client, server, message):
    """Called when a client sends a message"""
    if len(message) > 200:
        message = message[:200] + ".."
    print("Client(%d) command: %s" % (client["id"], message))
    command_output = shell(message, client, server)
    server.send_message(client, command_output)


PORT = 50000
IPADDR = "0.0.0.0"
server = WebsocketServer(PORT, IPADDR)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
