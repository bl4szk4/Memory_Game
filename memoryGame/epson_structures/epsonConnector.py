from pyModbusTCP.client import ModbusClient
from enums.epsonInstructions import Instructions


class Epson:
    """
    Class that manages connection with epson scara via ModbusTCP

    Attributes
    ----------
    :arg ip: ip of Epson Scara
    :arg port: port of connection
    :arg c: connection class of ModbusClient
    :arg actual_coord: coordinate selected by player
    :arg second_camera: should go to the last camera
    """
    def __init__(self):
        self.ip = '192.168.1.2'
        self.port = 502
        self.c = None
        self.actual_coord = 0
        self.second_camera = False

    def start_connection(self):
        """
        starts the connection
        """
        self.c = ModbusClient(host=self.ip, port=self.port, auto_open=True, timeout=3.0)
        if self.c.write_single_coil(Instructions.START_GAME.value, 1):
            self.reset_all()
            return 1
        else:
            self.c = None
            return 0

    def close_connection(self):
        """
        closes the connection
        """
        self.reset_all()
        self.c.write_single_coil(Instructions.START_GAME.value, 0)
        self.c.close()

    def write_coordinates(self, coordinates: int, go_camera: bool = False) -> bool:
        """
        Sends the point selected by the player/ai to follow by robot
        """
        self.c.write_single_coil(Instructions.PLACE_BACK.value, 0)

        if go_camera:
            response = self.c.write_single_coil(Instructions.NEW_COMMAND.value, 1)
            if not response:
                return False
        else:
            response = self.c.write_single_coil(Instructions.WITHOUT_CAMERA.value, 1)
            if not response:
                return False
        coordinates += 511
        self.actual_coord = coordinates
        response = self.c.write_single_coil(coordinates, 1)
        if not response:
            return False
        return True

    def get_response(self, instruction: Instructions) -> bool:
        """
        Gets response from epson
        :param instruction: which response to get
        :return: state of specific output bit
        """
        response = self.c.read_discrete_inputs(511, 3)
        if instruction == Instructions.CAMERA_POINT:
            return response[0]
        elif instruction == Instructions.HOME_POSITION:
            return response[1]
        elif instruction == Instructions.ELECTROMAGNET:
            return response[2]

    def place_back(self) -> bool:
        """
        Gives an instruction to place an item back on place and resets previously set coordinate bit
        :returns
        True if no error
        False if error
        """
        response = self.c.write_single_coil(Instructions.PLACE_BACK.value, 1)
        if not response:
            return False
        response = self.c.write_single_coil(Instructions.NEW_COMMAND.value, 0)
        if not response:
            return False
        response = self.c.write_single_coil(Instructions.WITHOUT_CAMERA.value, 0)
        if not response:
            return False
        response = self.c.write_single_coil(self.actual_coord, 0)
        if not response:
            return False
        return True

    def reset_all(self):
        """Resets all robot's coils"""
        for i in range(511, 544):
            self.c.write_single_coil(i, 0)

    def next_camera(self):
        """Gives instruction to go to the next camera point"""
        if not self.second_camera:
            self.c.write_single_coil(Instructions.GO_CAM_2.value, 1)
            self.second_camera = True
        else:
            self.c.write_single_coil(Instructions.GO_CAM_3.value, 1)
            self.second_camera = False

    def test_camera(self, start=False):
        """
        tests the camera position by giving instruction to the robot to take one element and move it to the camera pos
        :param start: True if it is start of the process
        """
        if start:
            self.c.write_single_coil(Instructions.TEST_CAMERA.value, 1)
        else:
            self.c.write_single_coil(Instructions.TEST_CAMERA.value, 0)
