from Movable3D import Movable3D
import numpy as np

class GroundTarget(Movable3D):
    def _initialize_route(self) -> None:
        self.steps = np.c_[(np.random.uniform(0.0, self.max_step, size=(self.number_of_steps, 2)), np.zeros((self.number_of_steps, 1)))]
        super()._initialize_route()