# `SimpleSim`
A complete environment for ***executing***, ***visualizing*** and ***generating data*** of simulated flights of an Unmanned Aerial Vehicle (UAV) 
chasing a ground target.

<p align="center">
    <img align="middle" src="https://github.com/Bilpapster/SimpleSim/blob/main/Repository%20resources/animation.gif" alt="SimpleSim animation example gif"/>
</p>


## 0. Basic Information
`SimpleSim` is originally developed by the author alongside with their participation in the [AIIA Laboratory](https://aiia.csd.auth.gr/) 
of the Aristotle University of Thessaloniki (AUTh). The simulator is written in `Python 3.9` programming language, making use of 
the `numpy` and `matplotlib` libraries. Fundamental math and physics equations are used behind the scenes, in combination with a pinch of artistic effort.


## 1. How to use `SimpleSim`
In order to use `SimpleSim`, you need to clone the current repository and run the following code in the project directory:

```python
from Simulator import Simulator

simulator = Simulator()
run_data = simulator.get_run_data()
simulator.visualize()
```


## 2. `SimpleSim` components
The `SimpleSim` environment composes of a UAV and a ground target. More details for each component are provided in the following sections

### 2.a. The UAV
The UAV is an abstraction of a flying object in the 3-dimensional space. It is equiped with a ***camera*** that surveils the ground, under a 
specific **angle** that is formed with respect to the horizontal axis. The camera field of view (FOV) has a specific **radius**, shaping a circle 
of view on the ground. Both the angle and the radius are totally customizable at creation time of the `Simulator` object.

### 2.b. The ground target
The ground target is an abstraction of an object moving on the ground (`z=0`) in the 3-dimensional space. Its trajectory is unrelated to the UAV's 
movement. Its route in the 3D space is totally customizable.


## 3. Visualizing the simulated run
`SimpleSim` provides a real-time, animated plot of the simulated run. The animated plot shows the UAV and target's route, as well as the UAV's 
trace (shadow) on the ground and the UAV's camera field of view on the ground. In order to visualize a randomly generated run, you can use the 
following code:

    Simulator().visualize()

The above concise, yet powerful, line of code yields a new window with an real-time animated plot of the above elements and an explanatory legend. 

## 4. Obtaining run data for further analysis or model training

Last but not least, `SimpleSim` provides an in-build method for accessing run data for both the UAV and the ground target. The data are structured
under a specially designed, two-leveled dictionary which can be accessed using the following code snippet:
```python
run_data_dict = Simulator().get_run_data()
```

Inside `run_data_dict` one can find the following hierarchy of stored data:
- `UAV`
    - `route`                                               (`ndarray`):  the exact coordinates (x, y, z) at every step of the UAV flight
    - `min_height`                                          (`float`):    the minimum height the UAV reached during flight
    - `max_height`                                          (`float`):    the maximum height the UAV reached during flight
    - `ground_trace_route`                                  (`ndarray`):  the exact coordinates (x, y, z) of the ground trace of the UAV 
                                                                          at every step of its flight
    - `camera_FOV_center`                                   (`ndarray`):  the exact coordinates (x, y, z) of the UAV camera field of view 
                                                                          center at every step of its flight
    - `camera_FOV_radius`                                   (`float`):    the radius of the UAV camera field of view center
    - `camera_FOV_angle_degrees`                            (`float`):    the angle (in degrees) that the UAV camera vision shapes with 
                                                                          the horizontal axis
    - `camera_target_miss_hits`                             (`ndarray`):  contains number_of_steps boolean values (True -> target inside 
                                                                          FOV at step i, False -> target outside FOV at step 1)
    - `camera_target_euclidean_distance_form_FOV_center`    (`ndarray`):  contains number_of_steps float values that represent the Euclidean distance 
                                                                          between the target and the camera field of view center at every step
    - `camera_target_manhattan_distance_form_FOV_center`    (`ndarray`):  contains number_of_steps float values that represent the Manhattan distance 
                                                                          between the target and the camera field of view center at every step

- `target`
    - `route`                                     (`ndarray`): the exact coordinates (x, y, z) at every step of the target movement


## 5. Future improvements

Using `SimpleSim` as the vehicle to run neural networks is an intriguiung idea that the author intends to implement, under the 
guidance of their AIIA Laboratory Supervisor.
