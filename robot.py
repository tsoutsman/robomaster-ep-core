#!/usr/bin/env python

import socket
import threading
from typing import ClassVar, Dict

import cv2
import numpy as np


class Robot:

    ROBOT_IP: str = "192.168.2.1"
    PORTS: ClassVar[Dict[str, int]] = {
        "video": 40921,
        "control": 40923,
        "event": 40925
    }

    def __init__(self) -> None:
        socket.setdefaulttimeout(5)
        sockets: Dict[str, socket.socket] = {
            "command": socket.socket(socket.AF_INET, socket.SOCK_STREAM),
            "video": socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        }

        self.threads: Dict[str, threading.Thread] = {
            "video": threading.Thread(target=get_video_stream)
        }

        self.video_on: bool = False
        self.video_stream: cv2.VideoCapture = None
        self.video_frame: np.ndarray = None

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

    def enable_video_stream(self) -> None:
        """Enables the robot's video stream."""
        self.video_on = True

        self.send_command("stream on")
        self.sockets["video"].connect((Robot.ROBOT_IP, Robot.PORTS["video"]))
        self.video_stream = cv2.VideoCapture(f"tcp://{Robot.ROBOT_IP}:{Robot.PORTS['video']}")

        self.threads["video"].start()

    def get_video_stream(self) -> None:
        """Continually updates the video stream. Used by seperate thread."""
        while True:
            ret: bool
            ret, self.video_frame = self.video_stream.read()
            if ret == False:
                print("Video stream read incorrectly")
            else:
                cv2.imshow("stream", self.video_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        self.video_stream.release()
        self.sockets["video"].shutdown(socket.SHUT_WR)
        self.sockets["video"].close()

    def read_video_stream(self) -> np.ndarray:
        """Access the current video frame.
        
        Returns:
            The current video frame.
        """
        return self.video_frame

    def disable_video_stream(self) -> None:
        """Disables the video stream."""
        self.video_on = False
        self.send_command("stream off")
