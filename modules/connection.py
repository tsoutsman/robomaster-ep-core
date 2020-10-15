#!/usr/bin/env python

import socket
from enum import Enum
from typing import Dict


class Port(Enum):
    video = 40921
    audio = 40922
    command = 40923
    message = 40924
    event = 40925
    broadcast = 40926
    all = 0


class Connection:

    IP: str = "192.168.2.1"

    def __init__(self):
        socket.setdefaulttimeout(5)
        self.sockets: Dict[Port, socket.socket] = {}

    def send(self, command) -> str:
        """Sends a command to the robot's command port

        Args:
            command: The command to be sent
        
        Returns:
            The robot's response
        
        Raises:
            AssertionError: If a connection to the robot's command port hasn't been established
        """
        assert (
            Port.command in self.sockets
        ), "A connection to the command port first needs to be established"

        if command[-1] != ";":
            command += ";"

        self.sockets[Port.command].send(command.encode("utf-8"))
        try:
            buf: str = self.sockets[Port.command].recv(1024)
            return buf.decode("utf-8")
        except socket.error as err:
            return f"Error receiving: {err}"

    def connect(self, port: Port) -> bool:
        """Connects to a robot's port.

        Args:
            port: The port to which to connect.
        
        Returns:
            The result of the connection. True if succesful, False otherwise.
        """
        self.sockets[port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sockets[port].connect(Connection.IP, port.value)
            if port == Port.command:
                self.send("command on;")
            return True
        except:
            return False

    def disconnect(self, port: Port) -> None:
        """Disconnects from a robot's port.

        Args:
            port: The port from which to disconnect.
        """
        if port == Port.all:
            [
                self.sockets[x].shutdown(socket.SHUT_WR).close()
                for x in self.sockets
            ]
        elif port in self.sockets:
            self.sockets[port].shutdown(socket.SHUT_WR)
            self.sockets[port].close()

    def get_ip(self) -> str:
        """Returns the robot's ip.

        Returns:
            The robot's ip.
        """
        return Connection.IP

    def get_sockets(self) -> Dict[Port, socket.socket]:
        """Returns all the current active sockets

        Returns:
            The current active sockets
        """
        return self.sockets
