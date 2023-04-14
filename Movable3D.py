import numpy as np

class Movable3D:
    """
    Represents an abstraction of a movable object in the 3D space.

    Attributes:
        - number_of_steps   (int):          The desired number of steps the object makes
        - max_step          (int):          The maximum step length the movable object can make towards each direction (x, y and z)
        - is_ground_movable (bool):         Defines whether the movable object is a ground object (stays in the same height during movement) or not
        - start_position    (array-like):   The start position (x, y, z) of the moving object.
        - steps             (ndarray):      A (number_of_steps x 3) numpy array containing the displacement towards each direction (x, y, z) 
                                            for every step of the object's movement
        - route             (ndarray):      A (number_of_steps x 3) numpy array containing the absolute coordinates (x, y, z) for every step 
                                            of the object's movement
    """

    def __init__(self, 
                 number_of_steps=1000, 
                 max_step=0.5, 
                 is_ground_movable=False, 
                 start_position = np.zeros(3)) -> None:
        """
        The constructor for Movable3D class.

        Args:
            number_of_steps     (int, optional):        The number of steps the movable object makes. Defaults to 1000.
            max_step            (float, optional):      The maximum step length the movable object can make towards each direction (x, y and z). Defaults to 0.5.
            is_ground_movable   (bool, optional):       Defines whether the movlable object is a ground object (stays in the same height during movement or not). Defaults to False.
            start_position      (array-like, optional): The coordinates (x, y, z) of the start of movement. Defaults to np.zeros(3).
        """
        self.number_of_steps = number_of_steps
        self.max_step = max_step
        self.is_ground_movable = is_ground_movable
        self.start_position = start_position
        self.steps = None
        self.route = None
        self._initialize_route()
        

    def _initialize_route(self) -> None:
        """
        (inside-class use only) Initializes the route of the movable object, based on the steps array. 
        """
        self._insert_turns()
        self.route = self.start_position + np.cumsum(self.steps, axis=0)
    

    def _insert_turns(self) -> None:
        """
        (inside-class use only) Randomly inserts 90-degrees turns (left and right) in the route.
        """
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
        """
        (inside-class use only) Defines the maximum height the movable object can reach during movement.
        """
        stop_elevation_time = np.random.randint(0, int(self.number_of_steps/2))
        self.route[(stop_elevation_time + 1):, 2] = self.route[stop_elevation_time, 2]