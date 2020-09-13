from robot import Robot
import cv2
import sys


def main():
    robot = Robot()
    robot.connect()
    robot.sendCommand("command on")

    robot.startVideoStream()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
