import numpy as np

class Movable3D:
    def __init__(self, 
                 number_of_steps=1000, 
                 max_step=0.5, 
                 is_ground_movable=False, 
                 start_position = np.zeros(3)) -> None:
        
        self.number_of_steps = number_of_steps
        self.max_step = max_step
        self.is_ground_movable = is_ground_movable
        self.start_position = start_position
        self.steps = None
        self.route = None
        self._initialize_route()
        

    def _initialize_route(self) -> None:
        if not self.is_ground_movable:
            self.steps = np.random.uniform(0.0, self.max_step, size=(self.number_of_steps, 3))
        else:
            self.steps = np.c_[(np.random.uniform(0.0, self.max_step, size=(self.number_of_steps, 2)), np.zeros((self.number_of_steps, 1)))]
        
        self._insert_turns()
        self.route = self.start_position + np.cumsum(self.steps, axis=0)
        self._set_maximum_height()
    

    def _insert_turns(self) -> None:
        number_of_turns = np.random.randint(0, int(self.number_of_steps/100) if self.number_of_steps >= 100 else 0)
        
        if number_of_turns == 0:
            return

        turn_start_times = np.random.randint(0, self.number_of_steps, size=(number_of_turns))
        turn_duration = int(self.number_of_steps/50) if self.number_of_steps > 50 else 1
        for turn_start_time in turn_start_times:
            left_or_right = np.random.randint(0, 2)
            self.steps[turn_start_time:(turn_start_time + turn_duration), left_or_right] = 0.
            self.steps[turn_start_time:(turn_start_time + turn_duration), 1 - left_or_right] *= 3
            self.steps[turn_start_time:(turn_start_time + turn_duration), 2] = 0.


    def _set_maximum_height(self) -> None:
        stop_elevation_time = np.random.randint(0, int(self.number_of_steps/2))
        self.route[(stop_elevation_time + 1):, 2] = self.route[stop_elevation_time, 2]