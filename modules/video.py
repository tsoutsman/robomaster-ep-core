#!/usr/bin/env python

import threading

import cv2
import numpy as np

from .connection import Connection, Port


class Video:
    def __init__(self, connection: Connection):
        self.__connection: Connection = connection
        self.__thread: threading.thread = threading.thread(
            target=self.__get_stream)
        self.__status: bool = False
        self.__stream: cv2.VideoCapture = None
        self.__current_frame: np.ndarray = None

    def enable(self) -> None:
        """Enables the video stream.

        Raises:
            AssertionError: If a connection to the robot's control port hasn't been established.
        """
        assert (
            self.__connection.get_sockets().get(Port.control)
        ), "A connection with the command port first needs to be established."

        self.__connection.connect(Port.video)
        self.__status = True
        self.__video_stream = cv2.VideoCapture(
            f"tcp://{self.__connection.get_ip()}:{Port.video.value}")
        self.thread.start()

    def disable(self) -> None:
        """Disables the video stream."""
        self.__status = False

    def read(self) -> np.ndarray:
        """Returns the current video frame.

        Returns:
            The current video frame
        """
        return self.current_frame

    def get_status(self) -> None:
        """Returns the state of the video stream.

        Returns:
            The status of the video stream. True if on, False if otherwise.
        """
        return self.__status

    def __get_stream(self) -> None:
        while self.__status:
            ret, self.current_frame = self.__stream.read()
        self.__stream.release()
