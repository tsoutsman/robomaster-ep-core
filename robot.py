# TODO: add multithreading to enable robot to do stuff while streaming video

import socket


class Robot:
    def __init__(self):
        self.s = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        s.connect(("192.168.2.1", 40923))
        print("Connected")

    def sendCommand(self, command):
        # sending command
        self.s.send(command.encode("utf-8"))

        # receiving command
        try:
            buf = self.s.recv(1024)
            return buf.decode("utf-8")
        except socket.error as e:
            return f"Error receiving: {e}"

    def commandMode(self, command):
        # enabling command mode
        sendCommand("command")
        while True:
            # quitting program
            if command.lower() == "q":
                break
            elif command.lower() == "video stream":
                enableVideoStream()
            # correcting syntax
            else:
                if command[-1] != ";":
                    command += ";"
                response = sendCommand(command)
                print(response)

        # Disable the port connection
        self.s.shutdown(socket.SHUT_WR)
        self.s.close()
