import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from Movable3D import Movable3D

class Simulator:
    def __init__(self, visualizationEnabled=True) -> None:
        self.UAV = Movable3D()
        self.target = Movable3D(is_ground_movable=True)
        self.UAV_ground_trace_route = self.UAV.route.copy()
        self.UAV_ground_trace_route[:, 2] = 0
        self.routes = [self.UAV.route, self.target.route, self.UAV_ground_trace_route]
        self.visualizationEnabled = visualizationEnabled
        self.visualization = None
        self.plot_handler = None
        self._initialize_plot_handler()

    
    def _initialize_plot_handler(self) -> None:
        self.plot_handler = {'UAV':{},
                             'target':{},
                             'UAV_ground_trace': {}}
        
        self.plot_handler['UAV']['color'] = mcolors.CSS4_COLORS['darkorchid']
        self.plot_handler['UAV']['linestyle'] = '-'
        self.plot_handler['UAV']['label'] = 'UAV'
        self.plot_handler['UAV']['alpha'] = 1

        self.plot_handler['UAV_ground_trace']['color'] = mcolors.CSS4_COLORS['slategrey']
        self.plot_handler['UAV_ground_trace']['linestyle'] = ':'
        self.plot_handler['UAV_ground_trace']['label'] = 'UAV ground trace'
        self.plot_handler['UAV_ground_trace']['alpha'] = 0.5

        self.plot_handler['target']['color'] = mcolors.CSS4_COLORS['lime']
        self.plot_handler['target']['linestyle'] = '--'
        self.plot_handler['target']['label'] = 'target'
        self.plot_handler['target']['alpha'] = 1


    def visualize(self):
        if not self.visualizationEnabled:
            print('Visualization is disabled for this instance.')
            return

        self.visualization = plt.figure(figsize=(8, 8))
        ax = self.visualization.add_subplot(projection='3d')
        ax.set(xlim3d=(0, 300), xlabel='X')
        ax.set(ylim3d=(0, 300), ylabel='Y')
        ax.set(zlim3d=(0, 300), zlabel='Z')
        ax.set(title='SimpleSim v1.0')

        trajectories = [ax.plot([], [], [], 
                                color=self.plot_handler[object_name]['color'],
                                linestyle=self.plot_handler[object_name]['linestyle'], 
                                alpha=self.plot_handler[object_name]['alpha'], 
                                label=self.plot_handler[object_name]['label'])[0] for object_name in self.plot_handler]

        animated_plot = animation.FuncAnimation(
            self.visualization, self._update_trajectories, self.UAV.number_of_steps, fargs=(self.routes, trajectories), interval=10,
        )
        plt.legend()
        plt.show()

    def _update_trajectories(self, current_number, walks, trajectories):
        for trajectory, route in zip(trajectories, self.routes):
            trajectory.set_data(route[:current_number, :2].T)
            trajectory.set_3d_properties(route[:current_number, 2])
        return trajectories
