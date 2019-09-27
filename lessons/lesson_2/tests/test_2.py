from ..glasses_2 import discofy_image as discofy_image
from ..glasses_2_solution import discofy_image as discofy_image_solution
import os
import filecmp


def test_solution():
    discofy_image_solution("team.png",
                           "disco-team.jpg")

    assert os.path.exists("disco-team.jpg"), \
        "oops, something's wrong with the solution"


def test_compare():
    discofy_image_solution("team.png",
                           "disco-team1.jpg")

    assert os.path.exists("disco-team1.jpg"), \
        "oops, something's wrong with the solution"

    discofy_image("team.png", "disco-team2.jpg")

    assert os.path.exists("disco-team2.jpg"), \
        "Your code is not generating an output file"

    assert filecmp.cmp("disco-team1.jpg",
                       "disco-team2.jpg",
                       shallow=False), "well, your solution did generate " \
                                       "something, but it is different from " \
                                       "our solution. open the images to " \
                                       "compare"

