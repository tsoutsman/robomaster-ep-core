#!/usr/bin/env python

import cv2

from robot import Robot


def main() -> None:
    robot = Robot()
    robot.connect()

    robot.start_video_stream()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
