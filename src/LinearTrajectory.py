class LinearTrajectory():
    def __init__(self, start_point, end_point, velocity, duration, dt) -> None:
        self.start_point = start_point
        self.end_point = end_point
        self.velocity = velocity
        self.duration = duration
        self.dt = dt
    

    def get_start_point(self):
        return self.start_point
    

    def get_end_point(self):
        return self.end_point
    

    def get_velocity(self):
        return self.velocity
    

    def get_duration(self):
        return self.duration
    

    def get_dt(self):
        return self.dt
    