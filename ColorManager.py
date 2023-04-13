import matplotlib.colors as mcolors

class ColorManager():
    def __init__(self) -> None:
        color_map = {}
        color_map['background'] = {'light': mcolors.CSS4_COLORS['whitesmoke'],
                                   'dark': mcolors.CSS4_COLORS['darkslategrey']}

        color_map['UAV'] =    {'light': mcolors.CSS4_COLORS['darkorchid'],
                               'dark': mcolors.CSS4_COLORS['hotpink']}
        
        color_map['UAV_ground_trace'] = {'light': mcolors.CSS4_COLORS['slategray'],
                                         'dark': mcolors.CSS4_COLORS['whitesmoke']}

        color_map['target'] = {'light': mcolors.CSS4_COLORS['lime'],
                               'dark': mcolors.CSS4_COLORS['greenyellow']}
        
        color_map['UAV_camera_FOV'] = {'light': mcolors.CSS4_COLORS['royalblue'],
                                       'dark': mcolors.CSS4_COLORS['conflowerblue']}
        
        
        