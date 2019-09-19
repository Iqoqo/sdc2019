from ..glasses_3 import discofy_image as discofy_image
from ..glasses_3_solution import discofy_image as discofy_image_solution
from ..glasses_3 import discofy_video as discofy_video
from ..glasses_3_solution import discofy_video as discofy_video_solution

import os
import filecmp


def test_solution_img():
    discofy_image_solution("team.png",
                           "disco-michael1.jpg")

    assert os.path.exists("disco-michael1.jpg"), \
        "oops, something's wrong with the solution"


def test_compare_img():
    discofy_image_solution("team.png",
                           "disco-michael1.jpg")

    assert os.path.exists("disco-michael1.jpg"), \
        "oops, something's wrong with the solution"

    discofy_image("team.png", "disco-michael2.jpg")

    assert os.path.exists("disco-michael2.jpg"), \
        "Your code is not generating an output file"

    assert filecmp.cmp("disco-michael1.jpg",
                       "disco-michael2.jpg",
                       shallow=False), "well, your solution did generate " \
                                       "something, but it is different from " \
                                       "our solution. open the images to " \
                                       "compare"


def test_solution_video():
    discofy_video_solution("samsungfun.mp4",
                           "disco-samsungfun1.mp4")

    assert os.path.exists("disco-samsungfun1.mp4"), \
        "oops, something's wrong with the solution"


def test_compare_video():
    discofy_video_solution("samsungfun.mp4",
                           "disco-samsungfun1.mp4")

    assert os.path.exists("disco-samsungfun1.mp4"), \
        "oops, something's wrong with the solution"

    discofy_video("samsungfun.mp4",
                  "disco-samsungfun2.mp4")

    assert os.path.exists("disco-samsungfun2.mp4"), \
        "oops, something's wrong with the solution"

    assert filecmp.cmp("disco-samsungfun1.mp4",
                       "disco-samsungfun2.mp4",
                       shallow=False), "well, your solution did generate " \
                                       "something, but it is different from " \
                                       "our solution. open the images to " \
                                       "compare"

