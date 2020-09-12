# TODO: add multithreading to enable robot to do stuff while streaming video

import socket
import cv2


class Robot:
    def __init__(self):
        self.command_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.command_s.connect(("192.168.2.1", 40923))

    def sendCommand(self, command):
        # sending command
        self.command_s.send(command.encode("utf-8"))

        # receiving command
        try:
            buf = self.command_s.recv(1024)
            return buf.decode("utf-8")
        except socket.error as e:
            return f"Error receiving: {e}"

    def commandMode(self):
        self.command_s.connect(("192.168.2.1", 40923))
        # enabling command mode
        sendCommand("command")
        while True:
            command = input("Command: ")
            # quitting program
            if command.lower() == "q":
                break
            # correcting syntax
            else:
                if command[-1] != ";":
                    command += ";"
                response = sendCommand(command)
                print(response)

        # Disable the port connection
        self.command_s.shutdown(socket.SHUT_WR)
        self.command_s.close()

    def videoStream(self):
        print(sendCommand("stream on"))
        self.video_s.connect(("192.168.2.1", 40921))

        video = cv2.VideoCapture()

        self.video_s.shutdown(socket.SHUT_WR)
        self.video_s.close()