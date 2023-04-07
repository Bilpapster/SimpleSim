from Movable3D import Movable3D
import numpy as np

class UAV(Movable3D):
    def _initialize_route(self) -> None:
        self.steps = np.random.uniform(0.0, self.max_step, size=(self.number_of_steps, 3))
        super()._initialize_route()
        self._set_maximum_height()
    