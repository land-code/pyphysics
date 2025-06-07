class Color:
    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def to_rgb(self):
        return (self.r, self.g, self.b)
