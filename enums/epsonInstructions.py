from enum import Enum


class Instructions(Enum):
    CAMERA_POINT = 0
    HOME_POSITION = 1
    ELECTROMAGNET = 3
    PLACE_BACK = 539
    NEW_COMMAND = 540
    WITHOUT_CAMERA = 541
    GO_CAM_2 = 542
    GO_CAM_3 = 543
    START_GAME = 544
    TEST_CAMERA = 545

