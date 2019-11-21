#!/usr/local/bin/python3

import numpy as np
import cv2
import dlib
import math
from imutils import face_utils, rotate_bound
import ffmpeg
import os
import glob
import sys
import imutils
import random

# consts
SHADES_LEFT_EYE_POS = (400, 450)
SHADES_RIGHT_EYE_POS = (1106, 450)
SHADES_EYE_DISTANCE = SHADES_RIGHT_EYE_POS[0] - SHADES_LEFT_EYE_POS[0]

ROOT_DIR = '/home/codelab'
OUT_DIR = './run-result'

# utility functions
def make_out_dir_safe():
    """
    Just make sure the output dir is there
    :return: None
    """
    dir_name = 'discofied'
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass
    return dir_name


def abs_path(rel_path):
    return os.path.join(ROOT_DIR, rel_path)


def default_output_name(input_name):
    """
    Generates a default output file for an input file
    :param input_name:
    :return:
    """
    paths = [OUT_DIR, f'disco_{input_name.split("/")[-1]}']
    return os.path.join(*paths)

def parse_args():
    """
    Parse arguments
        argv[1] in_file
    :return: args
    """
    in_file = None
    try:
        in_file = sys.argv[1]
    except IndexError:
        pass

    print(f"{in_file}")
    return in_file


def get_predictor():
    """
    :return: A predictor for face orientation.
    """
    return dlib.shape_predictor(abs_path('shape_predictor_68.dat'))


def get_detector():
    """
    :return: A face detector.
    """
    return dlib.get_frontal_face_detector()


# Image processing
def overlay_transparent(background, overlay, x, y):
    """
    Paste the overlay on the background image in position (x,y) .
    :param background: A background image.
    :param overlay: An overlay image. could be a PNG file with transparent
            background.
    :param x: x coordinate for the top left corner of the overlay image.
    :param y: y coordinate for the top left corner of the overlay image.
    :return: Mesh composition of overlay and background.
    """

    background_width = background.shape[1]
    background_height = background.shape[0]

    h, w = overlay.shape[0], overlay.shape[1]

    if (x >= background_width
            or y >= background_height
            or x + w < 0
            or y + h < 0):

        return background

    # cropping
    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    # handle out of bonds
    if x < 0:
        w = w + x
        overlay = overlay[:, -x:]
        x = 0

    if y < 0:
        h = h + y
        overlay = overlay[-y:]
        y = 0

    # calculate mask of overlay from
    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1),
                        dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    # separate mask from img
    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    # put all pieces together
    background_masked = (1.0 - mask) * background[y:y + h, x:x + w]
    overlay_masked = mask * overlay_image
    background[y:y + h, x:x + w] = background_masked + overlay_masked

    return background


def mesh_overlays(frame, shades_overlay, detector, predictor):
    """
    Use detector and predictor to find all face instances in the frame and
    mesh with overlay image after scale and orientation adjustments.
    :param frame: Frame image to process
    :param shades_overlay: Current overlay image
    :param detector: Face detector
    :param predictor: Orientation predictor
    :return: Processed image
    """
    out_frame = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)
    for rect in rects:
        # predictor used to detect orientation in place where current
        # face is
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # grab the outlines of each eye from the input image
        left_eye = shape[36:42]
        right_eye = shape[42:48]

        # compute the center of mass for each eye
        left_eye_center = left_eye.mean(axis=0).astype("int")
        right_eye_center = right_eye.mean(axis=0).astype("int")

        # compute the angle between the eye centroids
        d_y = left_eye_center[1] - right_eye_center[1]
        d_x = left_eye_center[0] - right_eye_center[0]

        angle = 180 + np.rad2deg(np.arctan2(d_y, d_x))

        # compute distance between eyes
        eye_distance = math.sqrt(int(d_y) ** 2 + int(d_x) ** 2)
        proportion = (1 / SHADES_EYE_DISTANCE) * eye_distance

        # resize shades to fit face width
        shades_shape = shades_overlay.shape[:2]

        resize_width = int(shades_shape[0] * proportion)
        resize_height = int(shades_shape[1] * proportion)
        shades_overlay_resized = cv2.resize(shades_overlay,
                                            (resize_height, resize_width))

        shades_overlay_resized = rotate_bound(shades_overlay_resized, angle)

        left_top_corner_x = int(left_eye_center[0]
                                - SHADES_LEFT_EYE_POS[0] * proportion)
        left_top_corner_y = int(left_eye_center[1]
                                - SHADES_LEFT_EYE_POS[1] * proportion)

        out_frame = overlay_transparent(out_frame,
                                        shades_overlay_resized,
                                        left_top_corner_x,
                                        left_top_corner_y)

    return out_frame


def discofy_image(in_image_path, out_image_path):
    #read the image 
    img = cv2.imread(in_image_path)
    
    #load the eyeglasses
    shades_overlay = cv2.imread(abs_path("glasses/disco_glasses_06.png"), cv2.IMREAD_UNCHANGED)

    detector = get_detector()
    predictor = get_predictor()

    out_frame = mesh_overlays(img, shades_overlay, detector, predictor)
    try:
        os.remove(out_image_path)
    except FileNotFoundError:
        pass

    cv2.imwrite(out_image_path, out_frame)


# main
def main():
    in_file = parse_args()
    if in_file is None:
        print("I need an input file to discofy. "
              "Be so kind and supply an image or video")
        return
    out_file = default_output_name(in_file)
    discofy_image(in_file, out_file)
    print ("Image Processed Successfully")

if __name__ == "__main__":
    main()
