from .vector import Vector
from .objects import DynamicObject, StaticObject, Ball, Rectangle, InclinedPlane
from PIL import ImageFont


class World:
    def __init__(self, width, height, gravity=Vector(0, 9.8)):
        self.width = width
        self.height = height
        self.gravity = gravity
        self.dynamic_objects = []
        self.static_objects = []

    def add_object(self, obj):
        if isinstance(obj, DynamicObject):
            self.dynamic_objects.append(obj)
        elif isinstance(obj, StaticObject):
            self.static_objects.append(obj)
        else:
            raise TypeError("Object must be a DynamicObject or StaticObject")

    def update(self, dt):
        for obj in self.dynamic_objects:
            # Peso
            obj.apply_force(self.gravity * obj.mass)

            # Colisiones entre objetos dinámicos
            for other_obj in self.dynamic_objects:
                if obj is other_obj:
                    continue

                if isinstance(obj, Ball) and isinstance(other_obj, Ball):
                    self.resolve_ball_collision(obj, other_obj)

                if isinstance(obj, Rectangle) and isinstance(other_obj, Ball):
                    self.resolve_rectangle_ball_collision(obj, other_obj)

            # Colisiones con planos inclinados
            for static_obj in self.static_objects:
                if isinstance(static_obj, InclinedPlane):
                    if isinstance(obj, Ball):
                        self.resolve_ball_inclined_collision(
                            obj, static_obj, dt)

            # Actualizar posición y velocidad
            obj.update(dt)

    def resolve_ball_collision(self, obj, other_obj):
        distance_vec = other_obj.position - obj.position
        distance = distance_vec.length()
        min_distance = obj.radius + other_obj.radius
        if distance < min_distance:
            # Resolver superposición
            overlap = min_distance - distance
            direction = distance_vec.normalize()
            obj.position -= direction * (overlap / 2)
            other_obj.position += direction * (overlap / 2)

            # Conservación de momento con restitución
            v1_n = obj.velocity.dot(direction)
            v2_n = other_obj.velocity.dot(direction)
            v1_t = obj.velocity - direction * v1_n
            v2_t = other_obj.velocity - direction * v2_n
            m1, m2 = obj.mass, other_obj.mass
            new_v1_n = (v1_n * (m1 - m2 * obj.restitution) +
                        2 * m2 * v2_n) / (m1 + m2)
            new_v2_n = (v2_n * (m2 - m1 * other_obj.restitution) +
                        2 * m1 * v1_n) / (m1 + m2)
            obj.velocity = v1_t + direction * new_v1_n
            other_obj.velocity = v2_t + direction * new_v2_n

    def resolve_rectangle_ball_collision(self, obj, other_obj):
        distance_vec = other_obj.position - obj.position
        distance = distance_vec.length()
        min_y = obj.height / 2 + other_obj.radius
        min_x = obj.width / 2 + other_obj.radius
        min_distance = min(min_y, min_x)
        if distance < min_distance:
            overlap = min_distance - distance
            direction = distance_vec.normalize()
            obj.position -= direction * (overlap / 2)
            other_obj.position += direction * (overlap / 2)

            v1_n = obj.velocity.dot(direction)
            v2_n = other_obj.velocity.dot(direction)
            v1_t = obj.velocity - direction * v1_n
            v2_t = other_obj.velocity - direction * v2_n
            m1, m2 = obj.mass, other_obj.mass
            new_v1_n = (v1_n * (m1 - m2 * obj.restitution) +
                        2 * m2 * v2_n) / (m1 + m2)
            new_v2_n = (v2_n * (m2 - m1 * other_obj.restitution) +
                        2 * m1 * v1_n) / (m1 + m2)
            obj.velocity = v1_t + direction * new_v1_n
            other_obj.velocity = v2_t + direction * new_v2_n

    def resolve_ball_inclined_collision(self, ball, plane, dt):
        plane_vec = plane.end_point - plane.start_point
        plane_length_sq = plane_vec.length() ** 2
        if plane_length_sq == 0:
            return

        ball_to_plane_start = ball.position - plane.start_point
        t = max(0, min(1, ball_to_plane_start.dot(plane_vec) / plane_length_sq))
        closest_point = plane.start_point + plane_vec * t
        distance_vec = ball.position - closest_point
        distance = distance_vec.length()

        if distance < ball.radius:
            overlap = ball.radius - distance
            collision_normal = plane.normal if distance == 0 else distance_vec.normalize()
            ball.position += collision_normal * overlap

            velocity_along_normal = ball.velocity.dot(collision_normal)

            if velocity_along_normal < 0:
                normal_force_magnitude = -velocity_along_normal * ball.mass / dt
                ball.apply_force(collision_normal * normal_force_magnitude)

                # Rebote inelástico
                ball.velocity -= collision_normal * ball.restitution * velocity_along_normal

                # Fuerza de rozamiento
                tangential_velocity = ball.velocity - \
                    collision_normal * ball.velocity.dot(collision_normal)
                if tangential_velocity.length() > 0:
                    friction_dir = tangential_velocity.normalize()
                    max_static = normal_force_magnitude * ball.static_friction
                    kinetic = tangential_velocity.length() * ball.mass / dt * ball.kinetic_friction
                    friction_force = -friction_dir * min(max_static, kinetic)
                    ball.apply_force(friction_force)

    def draw(self, draw):
        for static_obj in self.static_objects:
            static_obj.draw(draw)
        for obj in self.dynamic_objects:
            obj.draw(draw)
            label_info = obj.get_label_info()
            if label_info:
                font = ImageFont.load_default()
                draw.text((label_info["position"].x, label_info["position"].y),
                          label_info["text"],
                          fill=label_info["color"].to_rgb(),
                          font=font)
