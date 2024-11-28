class CenterScreen:
    def __init__(self, screen, win_width, win_height):
        self.window_width = win_width
        self.window_height = win_height
        middle_x = screen.winfo_screenwidth() // 2
        middle_y = screen.winfo_screenheight() // 2
        self.start_x = middle_x - self.window_width // 2
        self.start_y = middle_y - self.window_height // 2
