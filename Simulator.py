import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle
from ColorManager import ColorManager
from GroundTarget import GroundTarget
from UAV import UAV
import utilities as utils

# TO-DO: add docstrings and in-line comments

class Simulator:
    def __init__(self, visualizationEnabled=True, 
                 UAV_camera_FOV_angle_degrees=30, UAV_camera_FOV_radius=7.,
                 UAV_start_position=None, target_start_position=None,
                 theme='light') -> None:
        self.visualizationEnabled = visualizationEnabled
        self.UAV_camera_FOV_angle_degrees = UAV_camera_FOV_angle_degrees
        self.UAV_camera_FOV_radius = UAV_camera_FOV_radius
        self.color_manager = ColorManager(theme=theme)

        self._initialize_UAV(UAV_start_position)
        self._initialize_ground_target(target_start_position)
        self._initialize_plot_handler()

        self.routes = [self.UAV.route, self.target.route, self.UAV_ground_trace_route, self.UAV_camera_FOV_route]


    def _initialize_UAV(self, UAV_start_position) -> None:
        self.UAV = UAV() if UAV_start_position is None else UAV(start_position=UAV_start_position)
            
        self._initialize_UAV_ground_trace()
        self._initialize_UAV_camera_FOV()


    def _initialize_ground_target(self, target_start_position) -> None:
        self.target = GroundTarget() if target_start_position is None else GroundTarget(start_position=target_start_position)


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
        # self._initialize_plot_handler_UAV_camera_FOV()


    def _initialize_plot_hanlder_UAV(self) -> None:
        self.plot_handler['UAV'] = {'color': self.color_manager.get_color('UAV'),
                                    'linestyle': '-',
                                    'label': 'UAV',
                                    'marker': '4',
                                    'markersize': 15,
                                    'alpha': 1}

    
    def _initialize_plot_hander_UAV_ground_trace(self) -> None:
        self.plot_handler['UAV_ground_trace'] = {'color': self.color_manager.get_color('UAV_ground_trace'),
                                                 'linestyle': ':',
                                                 'label': 'UAV ground trace',
                                                 'marker': '.',
                                                 'markersize': None,
                                                 'alpha': 0.5}

    
    def _initialize_plot_handler_target(self) -> None:
        self.plot_handler['target'] = {'color': self.color_manager.get_color('target'),
                                       'linestyle': (5, (10, 3)), # long dash with offset
                                       'label': 'target',
                                       'marker':'X',
                                       'markersize': None,
                                       'alpha': 1}

    
    def _initialize_plot_handler_UAV_camera_FOV(self) -> None:
        self.plot_handler['UAV_camera_FOV'] = {'color': self.color_manager.get_color('UAV_camera_FOV'),
                                               'linestyle': ':',
                                               'label': 'UAV camera FOV center',
                                               'alpha': 0.8}


    def visualize(self) -> None:
        if not self.visualizationEnabled:
            print('Visualization is disabled for this instance.')
            return
        
        self._set_up_axis()
        trajectories = self._set_up_trajectories()
        UAV_camera_FOV = self._set_up_camera_FOV()
        trajectories.append(self.ax.add_patch(UAV_camera_FOV))
        art3d.pathpatch_2d_to_3d(UAV_camera_FOV, z=0.)
        animated_plot = animation.FuncAnimation(
            self.visualization, self._update_trajectories, self.UAV.number_of_steps, fargs=(self.routes, trajectories), interval=10, repeat=False
        )
        plt.legend(loc='best')
        plt.gca().set_facecolor(self.color_manager.get_color('background'))
        plt.show()


    def _set_up_axis(self) -> None:
        self.visualization = plt.figure(figsize=(8, 8))
        self.visualization.patch.set_facecolor(self.color_manager.get_color('background'))
        self.ax = self.visualization.add_subplot(111, projection='3d')
        max_ground_limit = np.max((self.UAV.route[-1, 0], self.UAV.route[-1, 1],
                                   self.target.route[-1, 0], self.target.route[-1, 1]))
        axis_view_offset = 10
        self.ax.set(xlim3d=(0, max_ground_limit + axis_view_offset), xlabel='X')
        self.ax.set(ylim3d=(0, max_ground_limit + axis_view_offset), ylabel='Y')
        self.ax.set(zlim3d=(0, self.UAV.route[-1, 2] + 10), zlabel='Z')
        # self.ax.set_axis_off()
        self.ax.set_title('SimpleSim v1.4', color=self.color_manager.get_color('foreground'), fontsize=20)


    def _set_up_trajectories(self) -> list:
        return [self.ax.plot([], [], [], 
                color=self.plot_handler.get(object).get('color'),
                linestyle=self.plot_handler.get(object).get('linestyle'), 
                alpha=self.plot_handler.get(object).get('alpha'), 
                marker=self.plot_handler.get(object).get('marker'),
                markersize=self.plot_handler.get(object).get('markersize'),
                label=self.plot_handler.get(object).get('label'))[0] for object in self.plot_handler]
    

    def _set_up_camera_FOV(self) -> Circle:
        return Circle(xy=(0,0), radius=0.)


    def _update_trajectories(self, current_number, walks, trajectories) -> list:
        for trajectory, route in zip(trajectories[:-1], self.routes):
            trajectory.set_data(route[(current_number-1):current_number, :2].T)
            trajectory.set_3d_properties(route[(current_number-1):current_number, 2])

        self.ax.patches[-1].remove()
        UAV_camera_FOV = Circle(xy=(self.UAV_camera_FOV_route[current_number, 0], self.UAV_camera_FOV_route[current_number, 1]),
                                radius=self.UAV_camera_FOV_radius,
                                color=self.color_manager.get_color('UAV_camera_FOV'),
                                label='camera FOV',
                                alpha=0.5)
        trajectories[-1] = self.ax.add_patch(UAV_camera_FOV)
        art3d.pathpatch_2d_to_3d(UAV_camera_FOV, z=0.)
        plt.legend(loc='best')
        return trajectories


    def get_run_data(self) -> dict:
        run_data = {}
        run_data['UAV'] = self._construct_run_data_UAV()
        run_data['target'] = self._construct_run_data_target()
        return run_data
    

    def _construct_run_data_UAV(self) -> dict:
        camera_target_miss_hits, camera_target_distance_from_FOV_center = self._compute_euclidean_distances()

        return {
            'route': self.UAV.route.copy(),
            'min_height': np.min(self.UAV.route[:, 2]),
            'max_height': np.max(self.UAV.route[:, 2]),
            'ground_trace_route': self.UAV_ground_trace_route.copy(),
            'camera_FOV_center': self.UAV_camera_FOV_route.copy(),
            'camera_FOV_radius': self.UAV_camera_FOV_radius,
            'camera_FOV_angle_degrees': self.UAV_camera_FOV_angle_degrees,
            'camera_target_miss_hits': np.array(camera_target_miss_hits),
            'camera_target_distance_from_FOV_center': np.array(camera_target_distance_from_FOV_center)
        }
    

    def _compute_euclidean_distances(self):
        camera_target_miss_hits = []
        camera_target_distance_from_FOV_center = []

        for UAV_coordinates, FOV_center_coordinates in zip(self.UAV.route, self.UAV_camera_FOV_route):
            UAV_coordinates = UAV_coordinates[:2]
            FOV_center_coordinates = FOV_center_coordinates[:2]
            euclidean_distance = utils.compute_euclidean_distance(UAV_coordinates, FOV_center_coordinates)
            camera_target_distance_from_FOV_center.append(euclidean_distance)
            camera_target_miss_hits.append(True if euclidean_distance <= self.UAV_camera_FOV_radius else False)

        return camera_target_miss_hits, camera_target_distance_from_FOV_center
    

    def _construct_run_data_target(self) -> dict:
        return {'route': self.target.route.copy()}
    