import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Movable3D import Movable3D

class Simulator:
    def __init__(self, visualizationEnabled=True) -> None:
        self.UAV = Movable3D()
        self.target = Movable3D(is_ground_movable=True)
        self.routes = [self.UAV.route, self.target.route]
        self.visualizationEnabled = visualizationEnabled
        self.visualization = None


    def visualize(self):
        if not self.visualizationEnabled:
            print('Visualization is disabled for this instance.')
            return

        self.visualization = plt.figure(figsize=(8, 8))
        ax = self.visualization.add_subplot(projection='3d')
        ax.set(xlim3d=(0, 300), xlabel='X')
        ax.set(ylim3d=(0, 300), ylabel='Y')
        ax.set(zlim3d=(0, 300), zlabel='Z')
        ax.set(title='SimpleSim v 0.1 - blue: UAV, orange: target')

        trajectories = [ax.plot([], [], [])[0] for _ in self.routes]

        animated_plot = animation.FuncAnimation(
            self.visualization, self._update_trajectories, self.UAV.number_of_steps, fargs=(self.routes, trajectories), interval=100,
        )
        plt.show()

    def _update_trajectories(self, current_number, walks, trajectories):
        for trajectory, route in zip(trajectories, self.routes):
            trajectory.set_data(route[:current_number, :2].T)
            trajectory.set_3d_properties(route[:current_number, 2])
        return trajectories
