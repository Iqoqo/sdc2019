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
INTERIM_VIDEO = 'interim.mp4'
SHADES_LEFT_EYE_POS = (400, 450)
SHADES_RIGHT_EYE_POS = (1106, 450)
SHADES_EYE_DISTANCE = SHADES_RIGHT_EYE_POS[0] - SHADES_LEFT_EYE_POS[0]

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


# utility functions
def abs_path(rel_path):
    return os.path.join(ROOT_DIR, rel_path)


def default_output_name(input_name):
    """
    Generates a default output file for an input file
    :param input_name:
    :return:
    """
    paths = input_name.split("/")[:-1] + [f'disco_{input_name.split("/")[-1]}']
    return os.path.join(*paths)


def parse_args():
    """
    Parse arguments
        argv[1] in_file
        argv[2] out_file
    :return: args
    """
    in_file = None
    out_file = None
    try:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    except IndexError:
        pass

    print(f"{in_file}, {out_file}")
    return in_file, out_file


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
    img = cv2.imread(in_image_path)
    shades_overlay = cv2.imread("disco_glasses.png", cv2.IMREAD_UNCHANGED)

    detector = get_detector()
    predictor = get_predictor()

    out_frame = mesh_overlays(img, shades_overlay, detector, predictor)
    try:
        os.remove(out_image_path)
    except FileNotFoundError:
        pass

    cv2.imwrite(out_image_path, out_frame)


def discofy_video(in_video_path, out_video_path):
    """
    Discofy a video.
    :param in_video_path: Path to input video
    :param out_video_path: Path to target output video. It is user's
            responsibility to make sure the target directory exists.
            If a file with the same name exists it will be overwritten.
    :return: None
    """
    detector = get_detector()
    predictor = get_predictor()

    # source video
    cap = cv2.VideoCapture(in_video_path)
    source_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    source_fps = int(cap.get(cv2.CAP_PROP_FPS))

    # video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(INTERIM_VIDEO,
                          fourcc,
                          source_fps,
                          (source_width, source_height))

    # We want the shades to be animated. So we prepared 12 images of the shades
    # with different glare. Following are the paths to all images.
    # In the video in frame i we want to take shades image i%12.
    # Don't forget to read images to memory with cv2.imread
    shades_paths = [abs_path(f"glasses/disco_glasses_{i:02d}.png")
                    for i in range(1, 13)]

    # loop over all images of the capture video.
    # Hint: ret, frame = cap.read().
    #       ret is true if the next frame is a valid image and false otherwise
    # Notice: In the last cap.read() ret is False. Ypu still have to write
    #         that frame to out to indicate the end of the video but you
    #         shouldn't do any image processing on it

    # while ???:
    #     read the next frame

    #     if not ret:
    #         out.write(frame)
    #         break

    #     find the right shades image
    #     mesh the shades to the image (use mesh_overlays)
    #     write the result image to the out video (Hint: out.write(frame))

    # Release capture devices
    cap.release()
    out.release()

    # Add sound to the video
    in1 = ffmpeg.input(INTERIM_VIDEO)
    in2 = ffmpeg.input(in_video_path)
    v1 = in1.video
    a2 = in2.audio
    out = ffmpeg.output(v1, a2, out_video_path)
    out.run(overwrite_output=True)

    # clear temp files
    os.remove(INTERIM_VIDEO)


def discofy_single(in_file, out_file):
    """
    Discofy a single file. Either an image or a video.
    :param in_file:
    :param out_file:
    :return:
    """
    if in_file.lower().endswith(('.png',
                                 '.jpg',
                                 '.jpeg',
                                 '.tiff',
                                 '.bmp',
                                 '.gif')):
        discofy_image(in_file, out_file)
    elif in_file.lower().endswith(('.mpg',
                                   '.mpeg',
                                   '.mp4',
                                   '.avi')):
        discofy_video(in_file, out_file)
    else:
        print("unsupported file format")
        return
    print(f'Discofied {in_file} to {out_file}')


# main
def main():
    in_file, out_file = parse_args()
    if in_file is None:
        print("I need an input file to discofy. "
              "Be so kind and supply an image or video")
        return
    out_file = out_file or default_output_name(in_file)
    discofy_single(in_file, out_file)


if __name__ == "__main__":
    main()
