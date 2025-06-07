import math
from dataclasses import dataclass

@dataclass
class Vector:
    """
    Representa un vector bidimensional con componentes x e y.
    """
    x: float
    y: float

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self.x / scalar, self.y / scalar)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        """Obtiene la longitud del vector"""
        return math.hypot(self.x, self.y)

    def normalize(self):
        """Devuelve un vector unitario de la misma dirección y sentido"""
        l = self.length()
        if l == 0:
            return Vector(0, 0)
        return self / l

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def rotate(self, angle_radians):
        """Rota el vector por el ángulo dado en radianes."""
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)
        return Vector(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a)
