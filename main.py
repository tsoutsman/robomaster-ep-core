from robot import Robot
import cv2


def main():
    robot = Robot()
    robot.connect()
    robot.startVideoStream()

    while True:
        ret, frame = robot.getVideoStream()
        if ret == False:
            print("Video stream read incorrectly")
        else:
            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()