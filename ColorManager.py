import matplotlib.colors as mcolors

class ColorManager():
    def __init__(self, theme='light') -> None:
        self.color_map = {}
        self.default_theme = 'light'
        self.theme = theme if theme in ('dark', 'light') else self.default_theme
        self.color_map['background'] = {'light': mcolors.CSS4_COLORS['whitesmoke'],
                                        'dark': mcolors.CSS4_COLORS['black']}
        
        self.color_map['foreground'] = {'light': mcolors.CSS4_COLORS['black'],
                                        'dark': mcolors.CSS4_COLORS['white']}

        self.color_map['UAV'] =    {'light': mcolors.CSS4_COLORS['darkorchid'],
                                    'dark': mcolors.CSS4_COLORS['magenta']}
        
        self.color_map['UAV_ground_trace'] = {'light': mcolors.CSS4_COLORS['slategray'],
                                              'dark': mcolors.CSS4_COLORS['snow']}

        self.color_map['target'] = {'light': mcolors.CSS4_COLORS['lime'],
                                    'dark': mcolors.CSS4_COLORS['greenyellow']}
        
        self.color_map['UAV_camera_FOV'] = {'light': mcolors.CSS4_COLORS['royalblue'],
                                            'dark': mcolors.CSS4_COLORS['cornflowerblue']}
        
    
    def set_theme(self, theme) -> None:
        self.theme = theme if theme in ('dark', 'light') else self.default_theme

    
    def get_color(self, key) -> int:
        return self.color_map.get(key).get(self.theme)

        