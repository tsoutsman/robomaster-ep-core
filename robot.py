#!/usr/bin/env python

import socket
from typing import ClassVar, Dict

import cv2
import numpy as np


def create_sockets():
    sockets: Dict[str, socket.socket] = {
        "command": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        "video": socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    }
    sockets["command"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets["video"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    [sockets[x].settimeout(5) for x in sockets]


class Robot:

    ROBOT_IP: str = "192.168.2.1"
    PORTS: ClassVar[Dict[str, int]] = {
        "video": 40921,
        "control": 40923,
        "event": 40925
    }

    def __init__(self) -> None:
        self.sockets: Dict[str, socket.socket] = create_sockets()

        self.video_on: bool = False
        self.video_stream: cv2.VideoCapture = None

    def connect(self) -> bool:
        """Initialises connection to robot over the command port.
        
        Returns:
            The return value. True for success, False otherwise.
        """
        try:
            self.sockets["command"].connect(
                (Robot.ROBOT_IP, Robot.PORTS["control"]))
        except socket.timeout as e:
            print("Error connecting")
            return False
        self.send_command("command on")
        return True

    def send_command(self, command: str) -> str:
        """Sends command to the robot.

        Args:
            command: The command to be sent to the robot.

        Returns:
            The robot's response.
        """
        # Correcting syntax
        if command[-1] != ";":
            command += ";"
        # Sending command
        self.sockets["command"].send(command.encode("utf-8"))

        # receiving command
        try:
            buf: str = self.sockets["command"].recv(1024)
            return buf.decode("utf-8")
        except socket.error as e:
            return f"Error receiving: {e}"

    def enable_command_mode(self) -> None:
        """Enables command mode."""
        self.sockets["command"].connect(
            (Robot.ROBOT_IP, Robot.PORTS["control"]))
        while True:
            command: str = input("Command: ")
            # exiting command mode
            if command.lower() == "q":
                break
            else:
                response: str = self.send_command(command)
                print(response)

        # Disable the port connection
        self.sockets["command"].shutdown(socket.SHUT_WR)
        self.sockets["command"].close()

    def start_video_stream(self) -> None:
        """Begins receiving the video stream on a seperate thread."""

        self.send_command("stream on")
        self.sockets["video"].connect((Robot.ROBOT_IP, Robot.PORTS["video"]))
        self.video_on = True

        self.video_stream = cv2.VideoCapture(
            f"tcp://{Robot.ROBOT_IP}:{Robot.PORTS['video']}")
        self.get_video_stream()

        self.sockets["video"].shutdown(socket.SHUT_WR)
        self.sockets["video"].close()

    def get_video_stream(self) -> None:
        """Continually updates the video stream."""
        while True:
            ret: bool
            ret, self.video_frame = self.video_stream.read()
            if ret == False:
                print("Video stream read incorrectly")
            else:
                cv2.imshow("frame", self.video_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        self.video_stream.release()

    def read_video_stream(self) -> np.ndarray:
        """Access the current video frame.
        
        Returns:
            The current video frame.
        """
        return self.video_frame
