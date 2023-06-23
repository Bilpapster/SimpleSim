class LinearTrajectory():
    def __init__(self, start_point, end_point, velocity, duration, d_t) -> None:
        self.start_point = start_point
        self.end_point = end_point
        self.velocity = velocity
        self.duration = duration
        self.d_t = d_t


    def get_start_point(self):
        """ Getter for the trajectory start position.
        """
        return self.start_point


    def get_end_point(self):
        """ Getter for the trajectory end position.
        """
        return self.end_point


    def get_velocity(self):
        """ Getter for the trajectory velocity.
        """
        return self.velocity


    def get_duration(self):
        """Getter for the trajecotry duration in milliseconds.
        """
        return self.duration


    def get_dt(self):
        """Getter for the trajecotry duration in milliseconds.
        """
        return self.d_t
    
