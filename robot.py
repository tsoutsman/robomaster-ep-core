#!/usr/bin/env python

from modules.connection import Connection, Port
from modules.smart import Smart
from modules.video import Video


class Robot:
    def __init__(self):
        self.connection = Connection()
        self.video = Video(self.connection)
        self.smart = Smart(self.video)

    def command_mode(self) -> None:
        """Enables the command mode, which sends commands to the robot based on user input.
        Should only be used for testing."""
        command: str = None
        while command.lower() != "q":
            if command:
                self.connection.send(command)
            command = input("[Robot]$ ")
