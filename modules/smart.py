#!/usr/bin/env python

import math

import numpy as np
from simple_pid import PID

from .utils.image import downscale, mask_colour
from .video import Video


class Smart:

    def __init__(self, video):
        self.video: Video = video
        # self.pid = PID(p, i, d)
        # self.pid.setpoint = 10

    def line_follow(self):
        pass

    def detect_line(self, img: np.ndarray, colour: str) -> np.ndarray:
        img = img.downscale(3)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = mask_colour(img, colour)
        img = cv2.Canny(img, 10, 10)
        return img
