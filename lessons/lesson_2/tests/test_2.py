from ..glasses_2 import discofy_image as discofy_image
from ..glasses_2_solution import discofy_image as discofy_image_solution
import os
import filecmp


def test_solution():
    discofy_image_solution("michael.jpg",
                           "disco-michael1.jpg")

    assert os.path.exists("disco-michael1.jpg"), \
        "oops, something's wrong with the solution"


def test_compare():
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

