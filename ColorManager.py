import matplotlib.colors as mcolors

class ColorManager():
    """
    A utility class for color management throughout the SimpleSim application.

    Attributes
        - color_map (dict): A 2-level dictionary containing colors for every element for both light and dark theme.
        - theme     (str) : The theme of the SimpleSim application ('light' or 'dark')
    """

    def __init__(self, theme='light') -> None:
        """
        The costructor for the ColorManager class.

        Args:
            theme (str, optional): The theme of the SimpleSim application (options: 'light' or 'dark'). Defaults to 'light'.
        """
        self.color_map = {}
        self.default_theme = 'light'
        self.theme = theme if theme in ('dark', 'light') else self.default_theme
        self.color_map['background'] = {'light': mcolors.CSS4_COLORS['lightgray'],
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
        """
        Sets the theme of the SimpleSim application to the desired value. Options: 'light' or 'dark'.

        Args:
            theme (str): The desired theme to set. If passed string is not in the options, the theme is set to default theme.
        """
        self.theme = theme if theme in ('dark', 'light') else self.default_theme

    
    def get_color(self, key) -> int:
        """
        Returns the color of the specified key-object, based on the current theme of the SimpleSim application.

        Args:
            key (str): The key-object to get the color of.

        Returns:
            int: the color code of the provided key-object, based on the current app theme.
        """
        return self.color_map.get(key).get(self.theme)

        