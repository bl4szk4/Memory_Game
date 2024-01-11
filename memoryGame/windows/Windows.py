class Windows:
    """
    Class that stores window parameters

    Attributes
    ----------
    :arg screen: screen that window is displayed on
    :arg screen_w: width of a window
    arg screen_h: height of a window
    """
    def __init__(self, screen, screen_w, screen_h):
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
