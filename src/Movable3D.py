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
                 number_of_steps=300, 
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
        self._initialize_random_route()
        

    def _initialize_random_route(self) -> None:
        """
        (inside-class use only) Initializes the route of the movable object, based on the steps array. 
        """
        self._initialize_random_steps()
        self._insert_random_turns()
        self.route = self.start_position + np.cumsum(self.steps, axis=0)

    def _initialize_random_steps(self) -> None:
        """
        (inside-class use only) Initializes the steps of the movable object, using a uniform distribution. 
        """
        self.steps = np.random.uniform(0.0, self.max_step, size=(self.number_of_steps, 3))
    

    def _insert_random_turns(self) -> None:
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


    def _set_random_maximum_height(self) -> None:
        """
        (inside-class use only) Defines the maximum height the movable object can reach during movement.
        """
        stop_elevation_time = np.random.randint(0, int(self.number_of_steps/2))
        self.route[(stop_elevation_time + 1):, 2] = self.route[stop_elevation_time, 2]


    def _set_linear_trajectory(self, start_point, end_point, velocity, duration, dt):
        # Calculate the number of steps
        num_steps = int(duration / dt)

        # Calculate the displacement vector
        displacement = end_point - start_point

        # Calculate the normalized direction vector
        direction = displacement / np.linalg.norm(displacement)

        # Calculate the step size
        step_size = velocity * dt

        # Initialize arrays to store the UAV's position at each time step
        position = np.zeros((num_steps, 3))

        # Simulation loop
        for i in range(num_steps):
            # Calculate the position at the current time step
            position[i] = start_point + direction * step_size * i

        self.route = position
        self.number_of_steps = num_steps
        return position


    def _simulate_orbit(self, center, radius, velocity, duration, dt):
        # Calculate the number of steps
        num_steps = int(duration / dt)

        # Calculate the angular velocity
        angular_velocity = velocity / radius

        # Initialize arrays to store the UAV's position at each time step
        position = np.zeros((num_steps, 3))

        # Simulation loop
        for i in range(num_steps):
            # Calculate the current angle based on time
            angle = angular_velocity * i * dt

            # Calculate the position at the current time step
            position[i] = center + np.array([radius * np.cos(angle), radius * np.sin(angle), 0])

        self.route = position
        self.number_of_steps = num_steps
        
    
    def _simulate_spiral_orbit(self, start_point, end_point, center, duration, dt):
        # Calculate the number of steps
        num_steps = int(duration / dt)

        # Calculate the displacement vectors
        displacement_start = start_point - center
        displacement_end = end_point - center

        # Calculate the radii of the circular orbits
        radius_start = np.linalg.norm(displacement_start)
        radius_end = np.linalg.norm(displacement_end)

        # Calculate the angular velocities
        angular_velocity_start = np.linalg.norm(np.cross(displacement_start, np.array([0, 0, 1]))) / radius_start
        angular_velocity_end = np.linalg.norm(np.cross(displacement_end, np.array([0, 0, 1]))) / radius_end

        # Initialize arrays to store the UAV's position at each time step
        position = np.zeros((num_steps, 3))

        # Simulation loop
        for i in range(num_steps):
            # Calculate the current angles based on time
            angle_start = angular_velocity_start * i * dt
            angle_end = angular_velocity_end * i * dt

            # Calculate the positions at the current time step
            position_start = center + np.array([radius_start * np.cos(angle_start), radius_start * np.sin(angle_start), 0])
            position_end = center + np.array([radius_end * np.cos(angle_end), radius_end * np.sin(angle_end), 0])

            # Interpolate between the start and end positions
            position[i] = (1 - i / num_steps) * position_start + (i / num_steps) * position_end

        self.route = position
        self.number_of_steps = num_steps
