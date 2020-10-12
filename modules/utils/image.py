#!/usr/bin/env python

import cv2
import numpy as np
from typing import Optional


def downscale(img: np.ndarray, percentage: Optional[int] = 50) -> np.ndarray:
    """Downscales image.

    Args:
        img: The image to be resized.
        percentage: The percentage of the height and width of the original image
            that the new image will be.
    
    Returns:
        The downscaled image.
    """
    width = int(img.shape[1] * percentage / 100)
    height = int(img.shape[0] * percentage / 100)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def mask_colour(img: np.ndarray, colour: str) -> np.ndarray:
    """Masks an image to only have a certain colour.

    Args:
        img: The image in an HSV format.
        colour: The colour to be masked.

    Returns:
        The resulting image.
    """
    colours = {
        "green": (np.array([20, 0, 165]), np.array([100, 120, 210])),
        "red": ((np.array([0, 70, 160]), np.array([8, 210, 255])))
    }
    lower, upper = colours[colour]
    mask = cv2.inRange(img, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
    return result