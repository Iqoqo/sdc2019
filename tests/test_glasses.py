from ..glasses_cv import overlay_transparent
from ..glasses_cv import get_detector
from ..glasses_cv import get_predictor
from ..glasses_cv import overlay_iterator
from ..glasses_cv import mesh_overlays
from ..glasses_cv import discofy_video
from ..glasses_cv import abs_path
from ..glasses_cv import discofy_image

import imutils
import pytest
import os
import cv2
import random


def test_out_of_bounds():
    current_glasses = cv2.imread(abs_path('tests/ooo_glasses.jpg'))
    out_frame = cv2.imread(abs_path('tests/ooo_frame.jpg'))
    left_eye_x, left_eye_y = 758, -39
    _ = overlay_transparent(out_frame, current_glasses, left_eye_x, left_eye_y)


@pytest.mark.parametrize('input_f', ['neta.jpg', 'shia.jpg'])
def test_single_frame(input_f):
    frame = cv2.imread(abs_path(f'tests/{input_f}'))
    detector = get_detector()
    predictor = get_predictor()
    overlays = overlay_iterator()

    shades_overlay = next(overlays)
    out_frame = mesh_overlays(frame, shades_overlay, detector, predictor)
    cv2.imwrite(abs_path(f'tests/mesh_{input_f}'), out_frame)


def test_short_only():
    print('short only')
    discofy_video(abs_path('videos/short.mp4'), 'bla.mp4')
    os.remove('bla.mp4')


@pytest.mark.parametrize('input_f',
                         ['Zohar.png', 'Yoad.png', 'Gilad.png', 'Hadas.png'])
def test_build_team(input_f):
    discofy_image(abs_path(f'misc/{input_f}'),
                  abs_path(f'misc/disco_{input_f}'),
                  do_resize=True)

