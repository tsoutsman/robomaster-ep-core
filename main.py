#!/usr/bin/env python

import cv2
from modules.connection import Port

from robot import Robot


def show_stream(robot: Robot) -> None:
    while True:
        frame = robot.video.read()
        try:
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        except:
            pass


def main() -> None:
    robot: Robot = Robot()
    robot.connection.connect(Port.command)
    robot.connection.connect(Port.video)
    robot.video.enable()
    show_stream(robot)
    robot.video.disable()
    robot.connection.disconnect(Port.all)


if __name__ == "__main__":
    main()
