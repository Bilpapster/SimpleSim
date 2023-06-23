import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle
from ColorManager import ColorManager
from GroundTarget import GroundTarget
from UAV import UAV
import utilities as utils


class Simulator:
    """
    Represents a simulator environment that executes runs. The environment contains an abstraction of an UAV (equiped with a camera) and a ground target. 

    The UAV is a flying Movable3D object that moves in the 3D space. It is equiped with a camera that focuses on the ground under a specific angle with the 
    horizontal axis. The UAV trajectory, as well as the UAV ground trace and the camera field of view (FOV) can be visualized in an animated 3D plot.

    The ground target is a ground Movable3D object that moves in the 3D space. It follows a trajectory on the ground (height is equal to 0) throughout its
    whole movement. Its trajectory is visualized in the same animated 3D plot as the UAV.
    
    Attributes:
        - visualizationEnabled      (bool):         Defines whether the environment can be visualized or not.
        - UAV                       (UAV):          The UAV object of the simulation.
        - UAV_start_position        (array-like):   The start position (x, y, z) of the UAV movement.
        - UAV_camera_FOV_degrees    (float):        The degrees the camera vision line shapes with the horizontal axis. 
        - UAV_camera_FOV_radius     (float):        The radius of the UAV camera FOV.
        - UAV_camera_FOV_route      (ndarray):      The route of the UAV FOV center.
        - UAV_ground_trace_route    (ndarray):      The trace (vertical shadow) of the UAV object on the ground. 
        - target                    (GroundTarget): The ground target object of the simulation.
        - target_start_position     (array-like):   The start position (x, y, z) of the ground target movement.
        - routes                    (ndarray):      An array that contains the routes of all the objects of the environment.
        - color_manager             (ColorManager): A custom class object for color and theme management throughout the environment.
        - theme                     (str):          The theme ('light' or 'dark') of the SimpleSim application.
        - plot_handler              (dict):         A special 2-level dictionary for plot management of the animated run.
        - ax                        (Axes):         The axes of the animated run.

    """

    def __init__(self, visualizationEnabled=True, 
                 UAV_camera_FOV_angle_degrees=70, UAV_camera_FOV_radius=1.,
                 UAV_start_position=None, target_start_position=None,
                 theme='light') -> None:
        """
        The constructor for the Simulator class. Creates the environment, initializes the objects, their routes, as 
        well as the color and plot management instances.

        Args:
            visualizationEnabled          (bool, optional):         Defines whether the visualization is enabled or not for this environment. Defaults to True.
            UAV_camera_FOV_angle_degrees  (float, optional):        The angle (in degrees) that the UAV camera vision shapes with the horizontal axis. 
                                                                    Defaults to 70°.
            UAV_camera_FOV_radius         (float, optional):        The radius of the UAV camera field of view (FOV). Defaults to 1.0.
            UAV_start_position            (array-like, optional):   The start position (x, y, z) of the UAV movement. Defaults to None, which leads to 
                                                                    Movable3D constructor default value.
            target_start_position         (array-like, optional):   The start position (x, y, z) of the ground target. Defaults to None, which leads to
                                                                    Movable3D constructor default value.
            theme                         (str, optional):          The theme (see ColorManager class for available options). Defaults to 'light'.
        """
        self.version = '1.8'

        self.visualizationEnabled = visualizationEnabled
        self.UAV_camera_FOV_angle_degrees = UAV_camera_FOV_angle_degrees
        self.UAV_camera_FOV_radius = UAV_camera_FOV_radius
        self.color_manager = ColorManager(theme=theme)

        self._initialize_UAV(UAV_start_position)
        self._initialize_ground_target(target_start_position)
        self._initialize_plot_handler()

        self.routes = [self.UAV.route, self.target.route, self.UAV_ground_trace_route, self.UAV_camera_FOV_route]


    def _initialize_UAV(self, UAV_start_position) -> None:
        """
        (for inside-class use only) Initializes the UAV object and its components.

        Args:
            UAV_start_position (array-like): The start position of the UAV object movement.
        """
        check_points = [np.array([0, 0, 0]), 
                        np.array([5, 12, 20]),
                        np.array([10, 5, 20]),
                        np.array([13, 20, 25]),
                        np.array([18, 13, 25]),
                        np.array([23, 21, 25])]   

        velocities = [2., 3., 4., 2., 1.5]   
        d_t = 0.1

        # temporarily, readability is to be enhanced soon! 
        self.UAV = UAV(check_points=check_points, velocities=velocities, d_t=d_t) if UAV_start_position is None else UAV(start_position=UAV_start_position, check_points=check_points, velocities=velocities, d_t=d_t)

        # self.UAV._set_linear_trajectory(start_point = np.array([0, 0, 10]), end_point=np.array([25, 28, 14]), velocity=1.5, duration=100, d_t=0.1)
           
        self._initialize_UAV_ground_trace()
        self._initialize_UAV_camera_FOV()


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
        # temporarily, readability is to be enhanced soon!
        self.target = GroundTarget(check_points=check_points, velocities=velocities, d_t=d_t) if target_start_position is None else GroundTarget(start_position=target_start_position, check_points=check_points, velocities=velocities, d_t=d_t)


    def _initialize_UAV_ground_trace(self) -> None:
        """
        (for inside-class use only) Initializes the ground trace (vertical shadow) of the UAV object on the ground.
        """
        self.UAV_ground_trace_route = self.UAV.route.copy()
        self.UAV_ground_trace_route[:, 2] = 0

    
    def _initialize_UAV_camera_FOV(self) -> None:
        """
        (for inside-class use only) Initializes the UAV camera field of view center and its route, based on the 
        angle of vision as well as the position of the UAV throughout its movement.
        """
        self.UAV_camera_FOV_route = self.UAV.route.copy()
        # self.UAV_camera_FOV_route[:, 1] -= np.tan(self.UAV_camera_FOV_angle_degrees * np.pi/180) * self.UAV_camera_FOV_route[:, 2]


        for step in range(self.UAV.number_of_steps):
            displacement_x, displacement_y = self._calculate_fov_center(float(step * 10), self.UAV_camera_FOV_angle_degrees)
            self.UAV_camera_FOV_route[step, 0] += displacement_x
            self.UAV_camera_FOV_route[step, 1] += displacement_y

        self.UAV_camera_FOV_route[:, 2] = 0.


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
        self._initialize_plot_hanlder_UAV()
        self._initialize_plot_handler_target()
        self._initialize_plot_hander_UAV_ground_trace()
        # self._initialize_plot_handler_UAV_camera_FOV()


    def _initialize_plot_hanlder_UAV(self) -> None:
        """
        (for inside-class use only) Initializes the plot handling object component that is responsible for the UAV.
        """
        self.plot_handler['UAV'] = {'color': self.color_manager.get_color('UAV'),
                                    'linestyle': ':',
                                    'label': 'UAV',
                                    'marker': '4',
                                    'markersize': 15,
                                    'alpha': 1}

    
    def _initialize_plot_hander_UAV_ground_trace(self) -> None:
        """
        (for inside-class use only) Initializes the plot handling object component that is responsible for the UAV trace on the ground.
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

    
    def _initialize_plot_handler_UAV_camera_FOV(self) -> None:
        """
        (for inside-class use only) Initializes the plot handling object component that is responsible for the UAV camera field of view.
        """
        self.plot_handler['UAV_camera_FOV'] = {'color': self.color_manager.get_color('UAV_camera_FOV'),
                                               'linestyle': ':',
                                               'label': 'UAV camera FOV center',
                                               'alpha': 0.5}


    def visualize(self) -> None:
        """
        Produces an animated 3-dimensional plot with the simulation elements, all in the same figure. The plot contains the trajectories 
        of the environment elements (animated), a title and a legend.
        """
        if not self.visualizationEnabled:
            print('Visualization is disabled for this instance.')
            return
        
        self._set_up_axis()
        trajectories = self._set_up_trajectories()
        UAV_camera_FOV = self._set_up_camera_FOV()
        trajectories.append(self.ax.add_patch(UAV_camera_FOV))
        art3d.pathpatch_2d_to_3d(UAV_camera_FOV, z=0.)
        trajectories.append(self.ax2.plot([], [], marker='X', color=self.color_manager.get_color('target'), label='target', linestyle='None'))

        # todo: find a more concise algorithmic way to discriminate the base trajectories from the trail ones

        # appends the trajectory of the UAV trail 
        trajectories.append(self.ax.plot([], [], [], 
                                         color=self.plot_handler.get('UAV').get('color'),
                                         linestyle=self.plot_handler.get('UAV').get('linestyle'), 
                                         alpha=self.plot_handler.get('UAV').get('alpha'), 
                                         label= '_UAV_trail')[0])
        
        # appends the trajectory of the target trail
        trajectories.append(self.ax.plot([], [], [], 
                                         color=self.plot_handler.get('target').get('color'),
                                         linestyle=self.plot_handler.get('target').get('linestyle'), 
                                         alpha=self.plot_handler.get('target').get('alpha'), 
                                         label= '_target_trail')[0])
        
        # appends the trajectory of the UAV ground trace
        trajectories.append(self.ax.plot([], [], [], 
                                         color=self.plot_handler.get('UAV_ground_trace').get('color'),
                                         linestyle=self.plot_handler.get('UAV_ground_trace').get('linestyle'), 
                                         alpha=self.plot_handler.get('UAV_ground_trace').get('alpha'), 
                                         label= '_UAV_ground_trace_trail')[0])


        animated_plot = animation.FuncAnimation(
            self.visualization, self._update_trajectories, self.UAV.number_of_steps, fargs=(self.routes, trajectories), interval=100, repeat=False
        )
        plt.show()


    def _set_up_axis(self) -> None:
        """
        (for inside-class use only) Sets up the axis for the animated, 3-dimensional plot and the camera FOV plot.
        """
        self.visualization = plt.figure(figsize=(20, 20), facecolor=self.color_manager.get_color('background'))
        self.visualization.patch.set_facecolor(self.color_manager.get_color('background'))
        self.ax = self.visualization.add_subplot(121, projection='3d')
        max_ground_limit = np.max((self.UAV.route[-1, 0], self.UAV.route[-1, 1],
                                   self.target.route[-1, 0], self.target.route[-1, 1]))
        axis_view_offset = 10
        self.ax.set(xlim3d=(0, max_ground_limit + axis_view_offset), xlabel='X')
        self.ax.set(ylim3d=(0, max_ground_limit + axis_view_offset), ylabel='Y')
        self.ax.set(zlim3d=(0, self.UAV.route[-1, 2] + 10), zlabel='Z')
        # self.ax.set_axis_off()
        self.ax.set_facecolor(self.color_manager.get_color('background'))
        self.ax.set_title('Live trajectories', fontsize=12)

        self.ax2 = self.visualization.add_subplot(122)

        self.ax2.plot(np.linspace(-1., 1., 10), np.zeros(10), color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_y=0')
        self.ax2.plot(np.zeros(10), np.linspace(-1., 1., 10), color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_x=0')

        x = np.linspace(-1./np.sqrt(2), 1./np.sqrt(2), 10)
        self.ax2.plot(x, x, color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_y=x')
        self.ax2.plot(x, -x, color=self.color_manager.get_color('foreground'), alpha = 0.1, linewidth=1.5, label='_y=-x')

        self.ax2.add_patch(Circle(xy=(0, 0), radius=1/3, edgecolor=self.color_manager.get_color('foreground'), linewidth=1.5, alpha=0.1, facecolor='None', label='_target-like circle 1'))
        self.ax2.add_patch(Circle(xy=(0, 0), radius=2/3, edgecolor=self.color_manager.get_color('foreground'), linewidth=1.5, alpha=0.1, facecolor='None', label='_target-like circle 2'))
        self.ax2.add_patch(Circle(xy=(0, 0), radius=1. , color= self.color_manager.get_color('UAV_camera_FOV'), alpha=0.3, label="camera FOV"))


        self.ax2.set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
        self.ax2.set_aspect(1.0/self.ax2.get_data_ratio(), adjustable='box')
        self.ax2.set_axis_off()
        self.ax2.set_title("UAV camera FOV", color=self.color_manager.get_color('foreground'), fontsize=12)

        self.visualization.suptitle(f'SimpleSim v{self.version}', color=self.color_manager.get_color('foreground'), fontsize=20)


    def _set_up_trajectories(self) -> list:
        """
        (for inside-class use only) Configures the initial state (placeholder) of the trajectories of the different elements of the 
        simulation (statically).

        Returns:
            list: a list of all the trajectories that are visualized in the 3-dimensional plot.
        """
        return [self.ax.plot([], [], [], 
                color=self.plot_handler.get(object).get('color'),
                linestyle=self.plot_handler.get(object).get('linestyle'), 
                alpha=self.plot_handler.get(object).get('alpha'), 
                marker=self.plot_handler.get(object).get('marker'),
                markersize=self.plot_handler.get(object).get('markersize'),
                label=self.plot_handler.get(object).get('label'))[0] for object in self.plot_handler]
    

    def _set_up_camera_FOV(self) -> Circle:
        """
        (for inside-class use only) Configures the initial state (palceholder) of the UAV camera field of view. The latter is a circle 
        with radius equal to value specified in the respective class attribute.

        Returns:
            Circle: The circle that represents the UAV camera field of view on the ground.
        """
        return Circle(xy=(0,0), radius=0.)


    def _update_trajectories(self, current_number, walks, trajectories) -> list:
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

        self.ax.patches[-1].remove()
        UAV_camera_FOV = Circle(xy=(self.UAV_camera_FOV_route[current_number, 0], self.UAV_camera_FOV_route[current_number, 1]),
                                radius=self.UAV_camera_FOV_radius,
                                color=self.color_manager.get_color('UAV_camera_FOV'),
                                label='camera FOV',
                                alpha=0.5)
        trajectories[-5] = self.ax.add_patch(UAV_camera_FOV)
        art3d.pathpatch_2d_to_3d(UAV_camera_FOV, z=0.)
        # plt.savefig('../skata/Figures/figure ' + str(current_number) + '.png')

        target_x_rescaled = (self.target.route[current_number, 0] - self.UAV_camera_FOV_route[current_number, 0]) / self.UAV_camera_FOV_radius   
        target_y_rescaled = (self.target.route[current_number, 1] - self.UAV_camera_FOV_route[current_number, 1]) / self.UAV_camera_FOV_radius
        trajectories[-4][0].set_data(target_x_rescaled, target_y_rescaled)

        # updates the UAV trajectory trail (trajectories[-3])
        trajectories[-3].set_data(self.UAV.route[:(current_number-1), :2].T)
        trajectories[-3].set_3d_properties(self.UAV.route[:(current_number-1), 2])

        # updates the target trajectory trail (trajectories[-2])
        trajectories[-2].set_data(self.target.route[:(current_number-1), :2].T)
        trajectories[-2].set_3d_properties(self.target.route[:(current_number-1), 2])

        # sets up the ground trace trajectory trail (trajectories[-1])
        trajectories[-1].set_data(self.UAV_ground_trace_route[:(current_number-1), :2].T)
        trajectories[-1].set_3d_properties(self.UAV_ground_trace_route[:(current_number-1), 2])

        legend_location = 'lower left'
        self.ax.legend(loc=legend_location)
        self.ax2.legend(loc=legend_location)
        return trajectories


    def get_run_data(self) -> dict:
        """
        Constructs and returns a special 2-leveled dictionary that contains the data of the current simulated run.
        The returned dictionary is 2-dimensional. The first dimension values are dictionaries themselves that contain
        as values the actual data. In particular, the dictionary has the following structure:
            - UAV (top level key)
                - route                                                 (ndarray):  the exact coordinates (x, y, z) at every step of the UAV flight
                - min_height                                            (float):    the minimum height the UAV reached during flight
                - max_height                                            (float):    the maximum height the UAV reached during flight
                - ground_trace_route                                    (ndarray):  the exact coordinates (x, y, z) of the ground trace of the UAV 
                                                                                    at every step of its flight
                - camera_FOV_center                                     (ndarray):  the exact coordinates (x, y, z) of the UAV camera field of view 
                                                                                    center at every step of its flight
                - camera_FOV_radius                                     (float):    the radius of the UAV camera field of view center
                - camera_FOV_angle_degrees                              (float):    the angle (in degrees) that the UAV camera vision shapes with 
                                                                                    the horizontal axis
                - camera_target_miss_hits                               (ndarray):  contains number_of_steps boolean values (True -> target inside 
                                                                                    FOV at step i, False -> target outside FOV at step 1)
                - camera_target_euclidean_distance_form_FOV_center      (ndarray):  contains number_of_steps float values that represent the Euclidean distance 
                                                                                    between the target and the camera field of view center at every step
                - camera_target_manhattan_distance_form_FOV_center      (ndarray):  contains number_of_steps float values that represent the Manhattan distance 
                                                                                    between the target and the camera field of view center at every step

            - target (top level key)
                - route                                                 (ndarray): the exact coordinates (x, y, z) at every step of the target movement


        Returns:
            dict: a 2-dimensional dictionary that contains the data of the current simulated run.
        """
        run_data = {}
        run_data['UAV'] = self._construct_run_data_UAV()
        run_data['target'] = self._construct_run_data_target()
        return run_data
    

    def _construct_run_data_UAV(self) -> dict:
        """
        (for inside-class use only) Constructs and returns the dictionary component of the run_data dictionary that is responsible 
        for the UAV data.

        Returns:
            dict: a dictionary that contains the data related to the UAV object of the current simulated run.
        """
        camera_target_miss_hits, camera_target_euclidean_distance_from_FOV_center, camera_target_manhattan_distance_from_FOV_center = self._compute_distances()

        return {
            'route': self.UAV.route.copy(),
            'min_height': np.min(self.UAV.route[:, 2]),
            'max_height': np.max(self.UAV.route[:, 2]),
            'ground_trace_route': self.UAV_ground_trace_route.copy(),
            'camera_FOV_center': self.UAV_camera_FOV_route.copy(),
            'camera_FOV_radius': self.UAV_camera_FOV_radius,
            'camera_FOV_angle_degrees': self.UAV_camera_FOV_angle_degrees,
            'camera_target_miss_hits': np.array(camera_target_miss_hits),
            'camera_target_euclidean_distance_from_FOV_center': np.array(camera_target_euclidean_distance_from_FOV_center),
            'camera_target_manhattan_distance_from_FOV_center': np.array(camera_target_manhattan_distance_from_FOV_center)
        }
    

    def _compute_distances(self):
        """
        (for inside-class use only) Computes the distance of the FOV center from the target at every step of the simulated flight and 
        constructs an numpy array containing this data, that is returned. It also returns a miss-hit array 
        (see get_run_data() method for more).

        Returns:
            ndarray: a numpy array that contains number_of_steps boolean values (True -> Hit, Flase -> Miss), one for every step of 
                     the simulated run
            ndarray: a numpy array that contains number_of_steps float values representing the distance between the UAV FOV center 
                     and the target at every step of the simulated run
        """
        camera_target_miss_hits = []
        camera_target_euclidean_distance_from_FOV_center = []
        camera_target_manhattan_distance_from_FOV_center = []

        for target_coordinates, FOV_center_coordinates in zip(self.target.route, self.UAV_camera_FOV_route):
            # keep only the (x, y) coordinates of the points, since they are on the ground (z=0)
            target_coordinates = target_coordinates[:2]
            FOV_center_coordinates = FOV_center_coordinates[:2]

            # compute the Euclidean distance and decide whether is a miss or a hit
            euclidean_distance = utils.compute_euclidean_distance(target_coordinates, FOV_center_coordinates)
            camera_target_euclidean_distance_from_FOV_center.append(euclidean_distance)
            camera_target_miss_hits.append(True if euclidean_distance <= self.UAV_camera_FOV_radius else False)

            # compute the Manhattan distance
            manhattan_distance = utils.compute_manhattan_distance(target_coordinates, FOV_center_coordinates)
            camera_target_manhattan_distance_from_FOV_center.append(manhattan_distance)


        return camera_target_miss_hits, camera_target_euclidean_distance_from_FOV_center, camera_target_manhattan_distance_from_FOV_center
    

    def _construct_run_data_target(self) -> dict:
        """
        (for inside-class use only) Constructs and returns the dictionary component of the run_data dictionary that is responsible for the target object data.

        Returns:
            dict: a dictionary that contains the data related to the target object of the current simulated run.
        """
        return {'route': self.target.route.copy()}
    
