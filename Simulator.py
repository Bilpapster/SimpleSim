import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle
from GroundTarget import GroundTarget
from UAV import UAV

class Simulator:
    def __init__(self, visualizationEnabled=True, UAV_camera_FOV_angle_degrees=150) -> None:
        self.visualizationEnabled = visualizationEnabled
        self.UAV_camera_FOV_angle_degrees = UAV_camera_FOV_angle_degrees

        self._initialize_UAV()
        self._initialize_ground_target()
        self._initialize_plot_handler()

        self.routes = [self.UAV.route, self.target.route, self.UAV_ground_trace_route, self.UAV_camera_FOV_route]


    def _initialize_UAV(self) -> None:
        self.UAV = UAV()
        self._initialize_UAV_ground_trace()
        self._initialize_UAV_camera_FOV()


    def _initialize_ground_target(self) -> None:
        self.target = GroundTarget()


    def _initialize_UAV_ground_trace(self) -> None:
        self.UAV_ground_trace_route = self.UAV.route.copy()
        self.UAV_ground_trace_route[:, 2] = 0

    
    def _initialize_UAV_camera_FOV(self) -> None:
        self.UAV_camera_FOV_route = self.UAV.route.copy()
        self.UAV_camera_FOV_route[:, 1] -= np.tan(self.UAV_camera_FOV_angle_degrees * np.pi/180) * self.UAV_camera_FOV_route[:, 2]
        self.UAV_camera_FOV_route[:, 2] = 0.


    def _initialize_plot_handler(self) -> None:
        self.plot_handler = {}
        self._initialize_plot_hanlder_UAV()
        self._initialize_plot_handler_target()
        self._initialize_plot_hander_UAV_ground_trace()
        self._initialize_plot_handler_UAV_camera_FOV()


    def _initialize_plot_hanlder_UAV(self) -> None:
        self.plot_handler['UAV'] = {'color': mcolors.CSS4_COLORS['darkorchid'],
                                    'linestyle': '-',
                                    'label': 'UAV',
                                    'alpha': 1}

    
    def _initialize_plot_hander_UAV_ground_trace(self) -> None:
        self.plot_handler['UAV_ground_trace'] = {'color': mcolors.CSS4_COLORS['slategrey'],
                                                 'linestyle': ':',
                                                 'label': 'UAV ground trace',
                                                 'alpha': 0.5}

    
    def _initialize_plot_handler_target(self) -> None:
        self.plot_handler['target'] = {'color': mcolors.CSS4_COLORS['lime'],
                                       'linestyle': (5, (10, 3)), # long dash with offset
                                       'label': 'target',
                                       'alpha': 1}

    
    def _initialize_plot_handler_UAV_camera_FOV(self):
        self.plot_handler['UAV_camera_FOV'] = {'color': mcolors.CSS4_COLORS['firebrick'],
                                               'linestyle': ':',
                                               'label': 'UAV camera FOV center',
                                               'alpha': 0.8}


    def visualize(self):
        if not self.visualizationEnabled:
            print('Visualization is disabled for this instance.')
            return

        self.visualization = plt.figure(figsize=(8, 8))
        self.ax = self.visualization.add_subplot(111, projection='3d')
        self.ax.set(xlim3d=(0, self.UAV.route[-1, 0] + 10), xlabel='X')
        self.ax.set(ylim3d=(0, self.UAV.route[-1, 1] + 10), ylabel='Y')
        self.ax.set(zlim3d=(0, self.UAV.route[-1, 2] + 10), zlabel='Z')
        # self.ax.set_axis_off()
        self.ax.set(title='SimpleSim v1.2')

        trajectories = [self.ax.plot([], [], [], 
                                color=self.plot_handler[object]['color'],
                                linestyle=self.plot_handler[object]['linestyle'], 
                                alpha=self.plot_handler[object]['alpha'], 
                                label=self.plot_handler[object]['label'])[0] for object in self.plot_handler]

        UAV_camera_FOV = Circle(xy=(0,0), 
                                radius=0., 
                                color='green', 
                                label = 'camera FOV',
                                alpha=0.5)
        trajectories.append(self.ax.add_patch(UAV_camera_FOV))
        art3d.pathpatch_2d_to_3d(UAV_camera_FOV, z=0.)

        animated_plot = animation.FuncAnimation(
            self.visualization, self._update_trajectories, self.UAV.number_of_steps, fargs=(self.routes, trajectories), interval=10, repeat=False
        )
        plt.legend(loc='best')
        plt.show()

    def _update_trajectories(self, current_number, walks, trajectories):
        for trajectory, route in zip(trajectories[:-1], self.routes):
            trajectory.set_data(route[:current_number, :2].T)
            trajectory.set_3d_properties(route[:current_number, 2])

        self.ax.patches[-1].remove()
        UAV_camera_FOV = Circle(xy=(self.UAV_camera_FOV_route[current_number, 0], self.UAV_camera_FOV_route[current_number, 1]),
                                radius=5.,
                                color=mcolors.CSS4_COLORS['red'],
                                label='camera FOV',
                                alpha=0.5)
        trajectories[-1] = self.ax.add_patch(UAV_camera_FOV)
        art3d.pathpatch_2d_to_3d(UAV_camera_FOV, z=0.)
        plt.legend(loc='best')
        return trajectories
