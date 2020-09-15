#!/usr/bin/env python

from robot import Robot
import cv2
import sys


def main():
    robot = Robot()
    robot.connect()

    robot.start_video_stream()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
