from PIL import ImageFont

from .vector import Vector
from .objects import DynamicObject, StaticObject, Ball, Rectangle, InclinedPlane
from .collisions import CollisionResolver


class World:
    def __init__(self, width, height, gravity=Vector(0, 500)):
        self.width = width
        self.height = height
        self.gravity = gravity
        self.objects = []
        self.collision_resolver = CollisionResolver()

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self, dt):
        # Aplicar gravedad y actualizar posición
        for obj in self.objects:
            if isinstance(obj, DynamicObject):
                obj.apply_force(self.gravity * obj.mass)

        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(dt)

        # Detectar y resolver colisiones entre objetos
        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i+1:]:
                self.collision_resolver.resolve(obj1, obj2, dt)

    def get_objects(self):
        return self.objects

    def draw(self, draw):
        for obj in self.objects:
            obj.draw(draw)
            if isinstance(obj, DynamicObject):
                label_info = obj.get_label_info()
                if label_info:
                    font = ImageFont.load_default()
                    draw.text((label_info["position"].x, label_info["position"].y),
                            label_info["text"],
                            fill=label_info["color"].to_rgb(),
                            font=font)
