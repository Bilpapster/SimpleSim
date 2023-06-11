from Movable3D import Movable3D
import numpy as np

class UAV(Movable3D):
    """
    Represents an Unmanned Aerial Vehicle (UAV) as a subclass of Movable3D class.
    """

    def _initialize_random_route(self) -> None:
        super()._initialize_random_route()
        self._set_random_maximum_height()
    