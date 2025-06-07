from PIL import ImageFont
import math

from .vector import Vector
from .color import Color

class DynamicObject:
    def __init__(self, position, mass, color=Color(255, 255, 255), restitution=0.5, static_friction=0.5, kinetic_friction=0.3, velocity=Vector(0, 0)):
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector(0, 0)
        self.mass = mass
        self.color = color
        # Coeficiente de restitución (0 = inelástico, 1 = elástico).
        self.restitution = restitution
        self.static_friction = static_friction
        self.kinetic_friction = kinetic_friction
        self.forces = Vector(0, 0)
        self.label = None

    def apply_force(self, force):
        self.forces += force

    def clear_forces(self):
        self.forces = Vector(0, 0)

    def update(self, dt):
        self.acceleration = self.forces / self.mass
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.clear_forces()

    def set_label(self, text, offset=Vector(0, -20), font_size=12, color=Color(255, 255, 255)):
        self.label = {"text": text, "offset": offset,
                      "font_size": font_size, "color": color}

    def get_label_info(self):
        if self.label:
            return {
                "text": f"{self.label['text']}\nPos: {self.position}\nVel: {self.velocity}",
                "position": self.position + self.label['offset'],
                "font_size": self.label['font_size'],
                "color": self.label['color']
            }
        return None

    def draw(self, draw):
        raise NotImplementedError


class Ball(DynamicObject):
    def __init__(self, position, radius, mass, color=Color(255, 0, 0), restitution=0.5, static_friction=0.5, kinetic_friction=0.3, velocity=Vector(0, 0)):
        super().__init__(position, mass, color, restitution,
                         static_friction, kinetic_friction, velocity)
        self.radius = radius

    def draw(self, draw):
        top_left = (int(self.position.x - self.radius),
                    int(self.position.y - self.radius))
        bottom_right = (int(self.position.x + self.radius),
                        int(self.position.y + self.radius))
        draw.ellipse([top_left, bottom_right], fill=self.color.to_rgb())


class Rectangle(DynamicObject):
    def __init__(self, position, width, height, mass, color=Color(0, 0, 255), restitution=0.5, static_friction=0.5, kinetic_friction=0.3, velocity=Vector(0, 0)):
        super().__init__(position, mass, color, restitution,
                         static_friction, kinetic_friction, velocity)
        self.width = width
        self.height = height

    def draw(self, draw):
        top_left = (int(self.position.x - self.width / 2),
                    int(self.position.y - self.height / 2))
        bottom_right = (int(self.position.x + self.width / 2),
                        int(self.position.y + self.height / 2))
        draw.rectangle([top_left, bottom_right], fill=self.color.to_rgb())

    def diagonal(self):
        return math.hypot(self.width, self.height)


class StaticObject:
    def __init__(self, color=Color(100, 100, 100)):
        self.color = color

    def draw(self, draw):
        raise NotImplementedError


class InclinedPlane(StaticObject):
    def __init__(self, start_point: Vector, end_point, color=Color(100, 100, 100)):
        super().__init__(color)
        self.start_point = start_point
        self.end_point = end_point
        self.normal = (self.end_point - self.start_point).normalize()
        # Normal apunta "hacia arriba"
        self.normal = Vector(-self.normal.y, self.normal.x)
        if self.normal.y < 0:  # Asegurarse de que la normal apunta hacia arriba
            self.normal = self.normal * -1
        self.length = (self.end_point - self.start_point).length()

    def draw(self, draw):
        draw.line([(self.start_point.x, self.start_point.y), (self.end_point.x, self.end_point.y)],
                  fill=self.color.to_rgb(), width=2)


class LabelTime(StaticObject):
    def __init__(self, position=Vector(10, 10), color=(255, 255, 255), font_path=None, font_size=18):
        super().__init__(color=color)
        self.position = position
        self.font_size = font_size
        self.font_path = font_path
        self.font = ImageFont.load_default(
        ) if font_path is None else ImageFont.truetype(font_path, font_size)
        self.time = 0.0
        self.text = "Time: 0.00 s"

    def update(self, dt):
        self.time += dt
        print(self.time)
        self.text = f"Time: {self.time:.2f} s"

    def draw(self, draw):
        draw.text((self.position.x, self.position.y),
                  self.text, font=self.font, fill=self.color)
