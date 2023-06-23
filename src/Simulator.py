import numpy as np

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle

from mpl_toolkits.mplot3d import art3d
from ColorManager import ColorManager
from GroundTarget import GroundTarget
from UAV import UAV
import utilities as utils


class Simulator:
    """
    Represents a simulator environment that executes runs. The environment contains an abstraction
     of an uav (equiped with a camera) and a ground target. 

    The uav is a flying Movable3D object that moves in the 3D space. It is equiped with a camera 
    on the ground under a specific angle with the horizontal axis. The uav trajectory, as well 
    as the uav ground trace and the camera field of view (fov) can be visualized in an animated 
    3D plot.

    The ground target is a ground Movable3D object that moves in the 3D space. It follows
    a trajectory on the ground (height is equal to 0) throughout its whole movement. 
    Its trajectory is visualized in the same animated 3D plot as the uav.
    
    Attributes:
        - visualization_enabled     (bool):         Defines whether the environment can be 
                                                    visualized or not.
        - uav                       (uav):          The uav object of the simulation.
        - uav_start_position        (array-like):   The start position (x, y, z) of the
                                                    UAV movement.
        - uav_camera_fov_degrees    (float):        The degrees the camera vision line shapes
                                                    with the horizontal axis.
        - uav_camera_fov_radius     (float):        The radius of the uav camera fov.
        - uav_camera_fov_route      (ndarray):      The route of the uav fov center.
        - uav_ground_trace_route    (ndarray):      The trace (vertical shadow) of the uav
                                                    object on the ground. 
        - target                    (GroundTarget): The ground target object of the simulation.
        - target_start_position     (array-like):   The start position (x, y, z) of the ground
                                                    target movement.
        - routes                    (ndarray):      An array that contains the routes of all the
                                                    objects of the environment.
        - color_manager             (ColorManager): A custom class object for color and theme
                                                    management throughout the environment.
        - theme                     (str):          The theme ('light' or 'dark') of the
                                                    SimpleSim application.
        - plot_handler              (dict):         A special 2-level dictionary for plot
                                                    management of the animated run.
        - a_x                        (Axes):         The axes of the animated run.

    """

    def __init__(self, visualization_enabled=True,
                 uav_camera_fov_angle_degrees=70, uav_camera_fov_radius=1.,
                 uav_start_position=None, target_start_position=None,
                 theme='light') -> None:
        """
        The constructor for the Simulator class. Creates the environment, initializes the objects,
        their routes, as well as the color and plot management instances.

        Args:
            visualization_enabled         (bool, optional):         Defines whether the 
                                                                    visualization
                                                                    is enabled or not for this 
                                                                    environment.
                                                                    Defaults to True.
            uav_camera_fov_angle_degrees  (float, optional):        The angle (in degrees) that
                                                                    the uav camera vision shapes 
                                                                    with the horizontal axis. 
                                                                    Defaults to 70°.
            uav_camera_fov_radius         (float, optional):        The radius of the uav camera 
                                                                    field of view (fov). Defaults
                                                                    to 1.0.
            uav_start_position            (array-like, optional):   The start position (x, y, z)
                                                                    of the uav movement. Defaults
                                                                    to None,
                                                                    which leads to Movable3D
                                                                    constructor default value.
            target_start_position         (array-like, optional):   The start position (x, y, z)
                                                                    of the ground target. Defaults 
                                                                    to None, which leads to
                                                                    Movable3D constructor default 
                                                                    value.
            theme                         (str, optional):          The theme (see ColorManager class
                                                                    for available options). Defaults 
                                                                    to 'light'.
        """
        self.version = '1.8'

        self.visualization_enabled = visualization_enabled
        self.uav_camera_fov_angle_degrees = uav_camera_fov_angle_degrees
        self.uav_camera_fov_radius = uav_camera_fov_radius
        self.color_manager = ColorManager(theme=theme)

        self.visualization = None
        self.a_x = None
        self.ax2 = None
        self.uav_ground_trace_route = None
        self.uav_camera_fov_route = None

        self._initialize_uav(uav_start_position)
        self._initialize_ground_target(target_start_position)
        self._initialize_plot_handler()

        self.routes = [self.uav.route, self.target.route, self.uav_ground_trace_route, self.uav_camera_fov_route]


    def _initialize_uav(self, uav_start_position) -> None:
        """
        (for inside-class use only) Initializes the uav object and its components.

        Args:
            uav_start_position (array-like): The start position of the uav object movement.
        """
        check_points = [np.array([0, 0, 0]), 
                        np.array([5, 12, 20]),
                        np.array([10, 5, 20]),
                        np.array([13, 20, 25]),
                        np.array([18, 13, 25]),
                        np.array([23, 21, 25])]   

        velocities = [2., 3., 4., 2., 1.5]   
        d_t = 0.1

        self.uav = UAV(check_points=check_points, velocities=velocities, d_t=d_t)
        if uav_start_position is not None:
            self.uav.start_position = uav_start_position

        self._initialize_uav_ground_trace()
        self._initialize_uav_camera_fov()


    def _initialize_ground_target(self, target_start_position) -> None:
        """
        (for inside-class use only) Initializes the ground target object.

        Args:
            target_start_position (array-like): The start position of the ground target object movement.
        """

        check_points = [np.array([0, 0, 0]), 
                        np.array([9, 13, 0]),
                        np.array([20, 19, 0]),
                        np.array([10, 25, 0]),
                        np.array([18, 10, 0]),
                        np.array([30, 30, 0])]   

        velocities = [3., 2., 2., 5., 1.]   
        d_t = 0.1

        self.target = GroundTarget(check_points=check_points, velocities=velocities, d_t=d_t)
        if target_start_position is not None:
            self.target = target_start_position


    def _initialize_uav_ground_trace(self) -> None:
        """
        (for inside-class use only) Initializes the ground trace (vertical shadow) of the uav object on the ground.
        """
        self.uav_ground_trace_route = self.uav.route.copy()
        self.uav_ground_trace_route[:, 2] = 0

    
    def _initialize_uav_camera_fov(self) -> None:
        """
        (for inside-class use only) Initializes the uav camera field of view center and its route, based on the 
        angle of vision as well as the position of the uav throughout its movement.
        """
        self.uav_camera_fov_route = self.uav.route.copy()


        for step in range(self.uav.number_of_steps):
            displacement_x, displacement_y = self._calculate_fov_center(float(step * 10), self.uav_camera_fov_angle_degrees)
            self.uav_camera_fov_route[step, 0] += displacement_x
            self.uav_camera_fov_route[step, 1] += displacement_y

        self.uav_camera_fov_route[:, 2] = 0.


    def _calculate_fov_center(self, yaw, fov_angle):
        # Convert yaw angle to radians
        yaw_rad = np.deg2rad(yaw)

        # Calculate the displacement in the x and y directions
        displacement_x = np.tan(np.deg2rad(fov_angle)) * np.sin(yaw_rad)
        displacement_y = np.tan(np.deg2rad(fov_angle)) * np.cos(yaw_rad)

        return displacement_x, displacement_y


    def _initialize_plot_handler(self) -> None:
        """
        (for inside-class use only) Initializes all the components of the plot handling object for the animated plot visualization.
        """
        self.plot_handler = {}
        self._initialize_plot_hanlder_uav()
        self._initialize_plot_handler_target()
        self._initialize_plot_hander_uav_ground_trace()


    def _initialize_plot_hanlder_uav(self) -> None:
        """
        (for inside-class use only) Initializes the plot handling object component that is responsible for the uav.
        """
        self.plot_handler['UAV'] = {'color': self.color_manager.get_color('UAV'),
                                    'linestyle': ':',
                                    'label': 'UAV',
                                    'marker': '4',
                                    'markersize': 15,
                                    'alpha': 1}


    def _initialize_plot_hander_uav_ground_trace(self) -> None:
        """
        (for inside-class use only) Initializes the plot handling object component that is responsible for the uav trace on the ground.
        """
        self.plot_handler['UAV_ground_trace'] = {'color': self.color_manager.get_color('UAV_ground_trace'),
                                                 'linestyle': ':',
                                                 'label': 'UAV ground trace',
                                                 'marker': '.',
                                                 'markersize': None,
                                                 'alpha': 0.5}


    def _initialize_plot_handler_target(self) -> None:
        """
        (for inside-class use only) Initializes the plot handling object component that is responsible for the ground target.
        """
        self.plot_handler['target'] = {'color': self.color_manager.get_color('target'),
                                       'linestyle': ':',
                                       'label': 'target',
                                       'marker':'x',
                                       'markersize': None,
                                       'alpha': 1}


    def _initialize_plot_handler_uav_camera_fov(self) -> None:
        """
        (for inside-class use only) Initializes the plot handling object component that is responsible for the uav camera field of view.
        """
        self.plot_handler['UAV_camera_FOV'] = {'color': self.color_manager.get_color('UAV_camera_FOV'),
                                               'linestyle': ':',
                                               'label': 'UAV camera fov center',
                                               'alpha': 0.5}


    def visualize(self) -> None:
        """
        Produces an animated 3-dimensional plot with the simulation elements, all in the same figure. The plot contains the trajectories 
        of the environment elements (animated), a title and a legend.
        """
        if not self.visualization_enabled:
            print('Visualization is disabled for this instance.')
            return

        self._set_up_axis()
        trajectories = self._set_up_trajectories()
        uav_camera_fov = self._set_up_camera_fov()
        trajectories.append(self.a_x.add_patch(uav_camera_fov))
        art3d.pathpatch_2d_to_3d(uav_camera_fov, z=0.)
        trajectories.append(self.ax2.plot([], [], marker='X', color=self.color_manager.get_color('target'), label='target', linestyle='None'))

        # appends the trajectory of the uav trail 
        trajectories.append(self.a_x.plot([], [], [], 
                                         color=self.plot_handler.get('UAV').get('color'),
                                         linestyle=self.plot_handler.get('UAV').get('linestyle'), 
                                         alpha=self.plot_handler.get('UAV').get('alpha'), 
                                         label= '_uav_trail')[0])

        # appends the trajectory of the target trail
        trajectories.append(self.a_x.plot([], [], [], 
                                         color=self.plot_handler.get('target').get('color'),
                                         linestyle=self.plot_handler.get('target').get('linestyle'), 
                                         alpha=self.plot_handler.get('target').get('alpha'), 
                                         label= '_target_trail')[0])

        # appends the trajectory of the uav ground trace
        trajectories.append(self.a_x.plot([], [], [], 
                                         color=self.plot_handler.get('UAV_ground_trace').get('color'),
                                         linestyle=self.plot_handler.get('UAV_ground_trace').get('linestyle'),
                                         alpha=self.plot_handler.get('UAV_ground_trace').get('alpha'),
                                         label= '_uav_ground_trace_trail')[0])


        animated_plot = animation.FuncAnimation(
            self.visualization, self._update_trajectories, self.uav.number_of_steps, fargs=(trajectories, ), interval=100, repeat=False
        )
        plt.show()


    def _set_up_axis(self) -> None:
        """
        (for inside-class use only) Sets up the axis for the animated, 3-dimensional plot and the camera fov plot.
        """
        self.visualization = plt.figure(figsize=(20, 20), facecolor=self.color_manager.get_color('background'))
        self.visualization.patch.set_facecolor(self.color_manager.get_color('background'))
        self.a_x = self.visualization.add_subplot(121, projection='3d')
        max_ground_limit = np.max((self.uav.route[-1, 0], self.uav.route[-1, 1],
                                   self.target.route[-1, 0], self.target.route[-1, 1]))
        axis_view_offset = 10
        self.a_x.set(xlim3d=(0, max_ground_limit + axis_view_offset), xlabel='X')
        self.a_x.set(ylim3d=(0, max_ground_limit + axis_view_offset), ylabel='Y')
        self.a_x.set(zlim3d=(0, self.uav.route[-1, 2] + 10), zlabel='Z')
        # self.a_x.set_axis_off()
        self.a_x.set_facecolor(self.color_manager.get_color('background'))
        self.a_x.set_title('Live trajectories', fontsize=12)

        self.ax2 = self.visualization.add_subplot(122)

        self.ax2.plot(np.linspace(-1., 1., 10), np.zeros(10), color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_y=0')
        self.ax2.plot(np.zeros(10), np.linspace(-1., 1., 10), color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_x=0')

        x = np.linspace(-1./np.sqrt(2), 1./np.sqrt(2), 10)
        self.ax2.plot(x, x, color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_y=x')
        self.ax2.plot(x, -x, color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_y=-x')

        self.ax2.add_patch(Circle(xy=(0, 0), radius=1/3, edgecolor=self.color_manager.get_color('foreground'), linewidth=1.5, alpha=0.1, facecolor='None', label='_target-like circle 1'))
        self.ax2.add_patch(Circle(xy=(0, 0), radius=2/3, edgecolor=self.color_manager.get_color('foreground'), linewidth=1.5, alpha=0.1, facecolor='None', label='_target-like circle 2'))
        self.ax2.add_patch(Circle(xy=(0, 0), radius=1. , color= self.color_manager.get_color('UAV_camera_FOV'), alpha=0.3, label="camera fov"))

        self.ax2.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
        self.ax2.set_aspect(1.0/self.ax2.get_data_ratio(), adjustable='box')
        self.ax2.set_axis_off()
        self.ax2.set_title("uav camera fov", color=self.color_manager.get_color('foreground'), fontsize=12)

        self.visualization.suptitle(f'SimpleSim v{self.version}', color=self.color_manager.get_color('foreground'), fontsize=20)


    def _set_up_trajectories(self) -> list:
        """
        (for inside-class use only) Configures the initial state (placeholder) of the trajectories of the different elements of the 
        simulation (statically).

        Returns:
            list: a list of all the trajectories that are visualized in the 3-dimensional plot.
        """
        return [self.a_x.plot([], [], [], 
                color=self.plot_handler.get(object).get('color'),
                linestyle=self.plot_handler.get(object).get('linestyle'), 
                alpha=self.plot_handler.get(object).get('alpha'), 
                marker=self.plot_handler.get(object).get('marker'),
                markersize=self.plot_handler.get(object).get('markersize'),
                label=self.plot_handler.get(object).get('label'))[0] for object in self.plot_handler]


    def _set_up_camera_fov(self) -> Circle:
        """
        (for inside-class use only) Configures the initial state (palceholder) of the uav camera field of view. The latter is a circle 
        with radius equal to value specified in the respective class attribute.

        Returns:
            Circle: The circle that represents the uav camera field of view on the ground.
        """
        return Circle(xy=(0,0), radius=0.)


    def _update_trajectories(self, current_number, trajectories) -> list:
        """
        (for inside-class use only) A method that is automatically calle by the FuncAnimation process. Updates the trajectories of the 
        different elements of the simulation to the current number of steps.

        Args:
            current_number (int): the current step of the animated plot
            walks (dummy): dummy argument
            trajectories (lsit): the active trajectories that are visualized in the 3-dimensional animated plot

        Returns:
            list: the updated trajectories that are going to be visualizd in the 3-dimensional animated plot
        """
        for trajectory, route in zip(trajectories[:-5], self.routes):
            trajectory.set_data(route[(current_number-1):current_number, :2].T)
            trajectory.set_3d_properties(route[(current_number-1):current_number, 2])

        self.a_x.patches[-1].remove()
        uav_camera_fov = Circle(xy=(self.uav_camera_fov_route[current_number, 0], self.uav_camera_fov_route[current_number, 1]),
                                radius=self.uav_camera_fov_radius,
                                color=self.color_manager.get_color('UAV_camera_FOV'),
                                label='camera FOV',
                                alpha=0.5)
        trajectories[-5] = self.a_x.add_patch(uav_camera_fov)
        art3d.pathpatch_2d_to_3d(uav_camera_fov, z=0.)

        target_x_rescaled = (self.target.route[current_number, 0] - self.uav_camera_fov_route[current_number, 0]) / self.uav_camera_fov_radius   
        target_y_rescaled = (self.target.route[current_number, 1] - self.uav_camera_fov_route[current_number, 1]) / self.uav_camera_fov_radius
        trajectories[-4][0].set_data(target_x_rescaled, target_y_rescaled)

        # updates the uav trajectory trail (trajectories[-3])
        trajectories[-3].set_data(self.uav.route[:(current_number-1), :2].T)
        trajectories[-3].set_3d_properties(self.uav.route[:(current_number-1), 2])

        # updates the target trajectory trail (trajectories[-2])
        trajectories[-2].set_data(self.target.route[:(current_number-1), :2].T)
        trajectories[-2].set_3d_properties(self.target.route[:(current_number-1), 2])

        # sets up the ground trace trajectory trail (trajectories[-1])
        trajectories[-1].set_data(self.uav_ground_trace_route[:(current_number-1), :2].T)
        trajectories[-1].set_3d_properties(self.uav_ground_trace_route[:(current_number-1), 2])

        legend_location = 'lower left'
        self.a_x.legend(loc=legend_location)
        self.ax2.legend(loc=legend_location)
        return trajectories


    def get_run_data(self) -> dict:
        """
        Constructs and returns a special 2-leveled dictionary that contains the data of the current simulated run.
        The returned dictionary is 2-dimensional. The first dimension values are dictionaries themselves that contain
        as values the actual data. In particular, the dictionary has the following structure:
            - uav (top level key)
                - route                                                 (ndarray):  the exact coordinates (x, y, z) at every step of the uav flight
                - min_height                                            (float):    the minimum height the uav reached during flight
                - max_height                                            (float):    the maximum height the uav reached during flight
                - ground_trace_route                                    (ndarray):  the exact coordinates (x, y, z) of the ground trace of the uav 
                                                                                    at every step of its flight
                - camera_fov_center                                     (ndarray):  the exact coordinates (x, y, z) of the uav camera field of view 
                                                                                    center at every step of its flight
                - camera_fov_radius                                     (float):    the radius of the uav camera field of view center
                - camera_fov_angle_degrees                              (float):    the angle (in degrees) that the uav camera vision shapes with 
                                                                                    the horizontal axis
                - camera_target_miss_hits                               (ndarray):  contains number_of_steps boolean values (True -> target inside 
                                                                                    fov at step i, False -> target outside fov at step 1)
                - camera_target_euclidean_distance_form_fov_center      (ndarray):  contains number_of_steps float values that represent the Euclidean distance 
                                                                                    between the target and the camera field of view center at every step
                - camera_target_manhattan_distance_form_fov_center      (ndarray):  contains number_of_steps float values that represent the Manhattan distance 
                                                                                    between the target and the camera field of view center at every step

            - target (top level key)
                - route                                                 (ndarray): the exact coordinates (x, y, z) at every step of the target movement


        Returns:
            dict: a 2-dimensional dictionary that contains the data of the current simulated run.
        """
        run_data = {}
        run_data['UAV'] = self._construct_run_data_uav()
        run_data['target'] = self._construct_run_data_target()
        return run_data


    def _construct_run_data_uav(self) -> dict:
        """
        (for inside-class use only) Constructs and returns the dictionary component of the run_data dictionary that is responsible 
        for the uav data.

        Returns:
            dict: a dictionary that contains the data related to the uav object of the current simulated run.
        """
        camera_target_miss_hits, camera_target_euclidean_distance_from_fov_center, camera_target_manhattan_distance_from_fov_center = self._compute_distances()

        return {
            'route': self.uav.route.copy(),
            'min_height': np.min(self.uav.route[:, 2]),
            'max_height': np.max(self.uav.route[:, 2]),
            'ground_trace_route': self.uav_ground_trace_route.copy(),
            'camera_fov_center': self.uav_camera_fov_route.copy(),
            'camera_fov_radius': self.uav_camera_fov_radius,
            'camera_fov_angle_degrees': self.uav_camera_fov_angle_degrees,
            'camera_target_miss_hits': np.array(camera_target_miss_hits),
            'camera_target_euclidean_distance_from_fov_center': np.array(camera_target_euclidean_distance_from_fov_center),
            'camera_target_manhattan_distance_from_fov_center': np.array(camera_target_manhattan_distance_from_fov_center)
        }


    def _compute_distances(self):
        """
        (for inside-class use only) Computes the distance of the fov center from the target at every step of the simulated flight and 
        constructs an numpy array containing this data, that is returned. It also returns a miss-hit array 
        (see get_run_data() method for more).

        Returns:
            ndarray: a numpy array that contains number_of_steps boolean values (True -> Hit, Flase -> Miss), one for every step of 
                     the simulated run
            ndarray: a numpy array that contains number_of_steps float values representing the distance between the uav fov center 
                     and the target at every step of the simulated run
        """
        camera_target_miss_hits = []
        camera_target_euclidean_distance_from_fov_center = []
        camera_target_manhattan_distance_from_fov_center = []

        for target_coordinates, fov_center_coordinates in zip(self.target.route, self.uav_camera_fov_route):
            # keep only the (x, y) coordinates of the points, since they are on the ground (z=0)
            target_coordinates = target_coordinates[:2]
            fov_center_coordinates = fov_center_coordinates[:2]

            # compute the Euclidean distance and decide whether is a miss or a hit
            euclidean_distance = utils.compute_euclidean_distance(target_coordinates, fov_center_coordinates)
            camera_target_euclidean_distance_from_fov_center.append(euclidean_distance)
            camera_target_miss_hits.append(True if euclidean_distance <= self.uav_camera_fov_radius else False)

            # compute the Manhattan distance
            manhattan_distance = utils.compute_manhattan_distance(target_coordinates, fov_center_coordinates)
            camera_target_manhattan_distance_from_fov_center.append(manhattan_distance)


        return camera_target_miss_hits, camera_target_euclidean_distance_from_fov_center, camera_target_manhattan_distance_from_fov_center


    def _construct_run_data_target(self) -> dict:
        """
        (for inside-class use only) Constructs and returns the dictionary component of the run_data dictionary that is responsible for the target object data.

        Returns:
            dict: a dictionary that contains the data related to the target object of the current simulated run.
        """
        return {'route': self.target.route.copy()}
