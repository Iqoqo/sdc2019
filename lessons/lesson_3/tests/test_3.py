from ..glasses_3 import discofy_image as discofy_image
from ..glasses_3_solution import discofy_image as discofy_image_solution
from ..glasses_3 import discofy_video as discofy_video
from ..glasses_3_solution import discofy_video as discofy_video_solution

import os
import filecmp


def test_solution_img():
    discofy_image_solution("michael.jpg",
                           "disco-michael1.jpg")

    assert os.path.exists("disco-michael1.jpg"), \
        "oops, something's wrong with the solution"


def test_compare_img():
    discofy_image_solution("michael.jpg",
                           "disco-michael1.jpg")

    assert os.path.exists("disco-michael1.jpg"), \
        "oops, something's wrong with the solution"

    discofy_image("michael.jpg", "disco-michael2.jpg")

    assert os.path.exists("disco-michael2.jpg"), \
        "Your code is not generating an output file"

    assert filecmp.cmp("disco-michael1.jpg",
                       "disco-michael2.jpg",
                       shallow=False), "well, your solution did generate " \
                                       "something, but it is different from " \
                                       "our solution. open the images to " \
                                       "compare"


def test_solution_video():
    discofy_video_solution("very_short.mp4",
                           "disco-very_short1.mp4")

    assert os.path.exists("disco-very_short1.mp4"), \
        "oops, something's wrong with the solution"


def test_compare_video():
    discofy_video_solution("very_short.mp4",
                           "disco-very_short1.mp4")

    assert os.path.exists("disco-very_short1.mp4"), \
        "oops, something's wrong with the solution"

    discofy_video("very_short.mp4",
                  "disco-very_short2.mp4")

    assert os.path.exists("disco-very_short2.mp4"), \
        "oops, something's wrong with the solution"

    assert filecmp.cmp("disco-very_short1.mp4",
                       "disco-very_short2.mp4",
                       shallow=False), "well, your solution did generate " \
                                       "something, but it is different from " \
                                       "our solution. open the images to " \
                                       "compare"

