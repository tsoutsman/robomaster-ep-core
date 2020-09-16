#!/usr/bin/env python

import cv2

from robot import Robot


def show_stream(robot: Robot) -> None:
    while True:
        frame = robot.read_video_stream()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def main() -> None:
    robot: Robot = Robot()
    robot.connect()

    robot.enable_video_stream()
    show_stream(robot)


if __name__ == "__main__":
    main()
