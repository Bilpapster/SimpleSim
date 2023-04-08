import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
from UAV import UAV
from GroundTarget import GroundTarget

class Simulator:
    def __init__(self, visualizationEnabled=True) -> None:
        self.UAV = UAV()
        self.target = GroundTarget()
        self.UAV_ground_trace_route = self.UAV.route.copy()
        self.UAV_ground_trace_route[:, 2] = 0

        self.UAV_camera_FOV_route = self.UAV.route.copy()
        self.UAV_camera_FOV_route[:, 1] -= np.tan(10* np.pi/180) * self.UAV_camera_FOV_route[:, 2]
        self.UAV_camera_FOV_route[:, 2] = 0.

        self.routes = [self.UAV.route, self.target.route, self.UAV_ground_trace_route, self.UAV_camera_FOV_route]
        self.visualizationEnabled = visualizationEnabled
        self.visualization = None
        self.plot_handler = None
        self._initialize_plot_handler()


    def _initialize_plot_handler(self) -> None:
        self.plot_handler = {'UAV':{},
                             'target':{},
                             'UAV_ground_trace': {},
                             'UAV_camera_FOV': {}}
        
        self._initialize_plot_hanlder_UAV()
        self._initialize_plot_hander_UAV_ground_trace()
        self._initialize_plot_handler_target()
        self._initialize_plot_handler_UAV_camera_FOV()


    def _initialize_plot_hanlder_UAV(self) -> None:
        self.plot_handler['UAV']['color'] = mcolors.CSS4_COLORS['darkorchid']
        self.plot_handler['UAV']['linestyle'] = '-'
        self.plot_handler['UAV']['label'] = 'UAV'
        self.plot_handler['UAV']['alpha'] = 1

    
    def _initialize_plot_hander_UAV_ground_trace(self) -> None:
        self.plot_handler['UAV_ground_trace']['color'] = mcolors.CSS4_COLORS['slategrey']
        self.plot_handler['UAV_ground_trace']['linestyle'] = ':'
        self.plot_handler['UAV_ground_trace']['label'] = 'UAV ground trace'
        self.plot_handler['UAV_ground_trace']['alpha'] = 0.5

    
    def _initialize_plot_handler_target(self) -> None:
        self.plot_handler['target']['color'] = mcolors.CSS4_COLORS['lime']
        self.plot_handler['target']['linestyle'] = (5, (10, 3)) # long dash with offset
        self.plot_handler['target']['label'] = 'target'
        self.plot_handler['target']['alpha'] = 1

    
    def _initialize_plot_handler_UAV_camera_FOV(self):
        self.plot_handler['UAV_camera_FOV']['color'] = mcolors.CSS4_COLORS['firebrick']
        self.plot_handler['UAV_camera_FOV']['linestyle'] = ':'
        self.plot_handler['UAV_camera_FOV']['label'] = 'UAV camera FOV'
        self.plot_handler['UAV_camera_FOV']['alpha'] = 0.8


    def visualize(self):
        if not self.visualizationEnabled:
            print('Visualization is disabled for this instance.')
            return

        self.visualization = plt.figure(figsize=(8, 8))
        ax = self.visualization.add_subplot(projection='3d')
        ax.set(xlim3d=(0, 300), xlabel='X')
        ax.set(ylim3d=(0, 300), ylabel='Y')
        ax.set(zlim3d=(0, self.UAV.route[-1, 2] + 20), zlabel='Z')
        ax.set(title='SimpleSim v1.0')

        trajectories = [ax.plot([], [], [], 
                                color=self.plot_handler[object]['color'],
                                linestyle=self.plot_handler[object]['linestyle'], 
                                alpha=self.plot_handler[object]['alpha'], 
                                label=self.plot_handler[object]['label'])[0] for object in self.plot_handler]

        animated_plot = animation.FuncAnimation(
            self.visualization, self._update_trajectories, self.UAV.number_of_steps, fargs=(self.routes, trajectories), interval=10, repeat=False
        )
        plt.legend(loc='best')
        plt.show()

    def _update_trajectories(self, current_number, walks, trajectories):
        for trajectory, route in zip(trajectories, self.routes):
            trajectory.set_data(route[:current_number, :2].T)
            trajectory.set_3d_properties(route[:current_number, 2])
        return trajectories
