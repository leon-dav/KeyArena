import config

class Level1():
    def __init__(self):

        wx = config.APPLICATION_WIDTH
        wy = config.APPLICATION_HEIGTH

        size = 5

        def square_builder(vx, vy, size=size, color=(0, 0, 0)):
            return {"points": ((wx*vx-size, wy*vy-size), (wx*vx-size, wy*vy+size), (wx*vx+size, wy*vy+size), (wx*vx+size, wy*vy-size)), "color": color},
    

        self.OBSTACLES = [
            {"points": ((-5, -5), (wx+5, -5), (wx+5, 5), (-5, 5)), "color": (0, 0, 0)},
            {"points": ((wx+5, -5), (wx+5, wy+5), (wx-5, wy+5), (wx-5, -5)), "color": (0, 0, 0)},
            {"points": ((-5, wy-5), (wx+5, wy-5), (wx+5, wy+5), (-5, wy+5)), "color": (0, 0, 0)},
            {"points": ((-5, -5), (5, -5), (5, wy+5), (-5, wy-5)), "color": (0, 0, 0)},

            # others
            *square_builder(15/50, 35/50, 20),
            *square_builder(10/50, 25/50, 10),
            *square_builder(20/50, 25/50, 30),
            *square_builder(30/50, 29/50, 25),
            *square_builder(25/50, 1, 40),
            *square_builder(35/50, 10/50, 15),
            *square_builder(32/50, 14/50, 19),
            *square_builder(38/50, 23/50, 25),
            *square_builder(37/50, 30/50, 10),
            *square_builder(1, 20/50, 30),
            *square_builder(10/50, 10/50, 30),
        ]

        self.SCOREZONES = [
            [wx/2, wy/50*10, 100],
            [wx/8, wy/50*40, 100],
            [wx/8*7, wy/50*40, 100],
        ]
