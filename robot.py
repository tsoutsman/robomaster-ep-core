# TODO: add multithreading to enable robot to do stuff while streaming video

import socket
import cv2


class Robot:

    ROBOT_IP = "192.168.2.1"

    def __init__(self):
        self.command_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_on = False
        self.video_stream = None

        self.command_s.settimeout(10)

    def connect(self):
        self.command_s.connect((Robot.ROBOT_IP, 40923))
        # enabling command mode
        print("Connected")

    def sendCommand(self, command):
        # correcting syntax
        if command[-1] != ";":
            command += ";"
        # sending command
        self.command_s.send(command.encode("utf-8"))

        # receiving command
        try:
            buf = self.command_s.recv(1024)
            return buf.decode("utf-8")
        except socket.error as e:
            return f"Error receiving: {e}"

    def commandMode(self):
        self.command_s.connect((Robot.ROBOT_IP, 40923))
        while True:
            command = input("Command: ")
            # quitting program
            if command.lower() == "q":
                break
            else:
                response = self.sendCommand(command)
                print(response)

        # Disable the port connection
        self.command_s.shutdown(socket.SHUT_WR)
        self.command_s.close()

    def startVideoStream(self):
        self.sendCommand("stream on")
        self.video_s.connect((Robot.ROBOT_IP, 40921))
        self.video_on = True

        self.video_stream = cv2.VideoCapture(f"tcp://{Robot.ROBOT_IP}:40921")
        self.getVideoStream()

        self.video_s.shutdown(socket.SHUT_WR)
        self.video_s.close()

    def getVideoStream(self):
        """Seperate function used for threading"""
        while True:
            ret, frame = self.video_stream.read()
            if ret == False:
                print("Video stream read incorrectly")
            else:
                cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.video_stream.release()

    def readVideoStream(self):
        """Used by external program"""
        return self.video_frame
