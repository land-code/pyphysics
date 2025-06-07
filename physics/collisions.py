from .objects import Ball, Rectangle, InclinedPlane
from .vector import Vector

class CollisionResolver:
    def resolve(self, obj1, obj2, dt):
        types = {type(obj1), type(obj2)}

        if types == {Ball}:
            self.resolve_ball_collision(obj1, obj2)
        elif types == {Rectangle, Ball}:
            if isinstance(obj1, Rectangle):
                self.resolve_rectangle_ball_collision(obj1, obj2)
            else:
                self.resolve_rectangle_ball_collision(obj2, obj1)
        elif (isinstance(obj1, Ball) and isinstance(obj2, InclinedPlane)) or \
             (isinstance(obj2, Ball) and isinstance(obj1, InclinedPlane)):
            ball = obj1 if isinstance(obj1, Ball) else obj2
            plane = obj2 if isinstance(obj2, InclinedPlane) else obj1
            self.resolve_ball_inclined_collision(ball, plane, dt)
        # TODO: Añadir más colisiones

    def _resolve_collision_with_momentum(self, obj1, obj2, direction):
        v1_n = obj1.velocity.dot(direction)
        v2_n = obj2.velocity.dot(direction)
        v1_t = obj1.velocity - direction * v1_n
        v2_t = obj2.velocity - direction * v2_n
        m1, m2 = obj1.mass, obj2.mass
        new_v1_n = (v1_n * (m1 - m2 * obj1.restitution) +
                    2 * m2 * v2_n) / (m1 + m2)
        new_v2_n = (v2_n * (m2 - m1 * obj2.restitution) +
                    2 * m1 * v1_n) / (m1 + m2)
        obj1.velocity = v1_t + direction * new_v1_n
        obj2.velocity = v2_t + direction * new_v2_n

    def resolve_ball_collision(self, ball1, ball2):
        distance_vec = ball2.position - ball1.position
        distance = distance_vec.length()
        min_distance = ball1.radius + ball2.radius
        if distance < min_distance:
            overlap = min_distance - distance
            direction = distance_vec.normalize()
            # Separar objetos
            ball1.position -= direction * (overlap / 2)
            ball2.position += direction * (overlap / 2)

            self._resolve_collision_with_momentum(ball1, ball2, direction)

    def resolve_rectangle_ball_collision(self, rect, ball):
        distance_vec = ball.position - rect.position
        # Limitar la distancia para detectar colisión con rectángulo (aproximado)
        half_width = rect.width / 2
        half_height = rect.height / 2


        # Para evitar hacer overlap circular, limitamos el vector distancia en x e y por los semilados del rectángulo
        clamped_x = max(-half_width, min(distance_vec.x, half_width))
        clamped_y = max(-half_height, min(distance_vec.y, half_height))

        closest_point = rect.position + Vector(clamped_x, clamped_y)
        collision_vec = ball.position - closest_point
        distance = collision_vec.length()

        if distance < ball.radius:
            overlap = ball.radius - distance
            if distance == 0:
                # Si están exactamente superpuestos, tomamos una normal arbitraria
                direction = Vector(1, 0)
            else:
                direction = collision_vec.normalize()

            separation = direction * overlap
            ball.position += separation
            rect.position -= separation * 0.3  # El rectángulo es más pesado

            self._resolve_collision_with_momentum(rect, ball, direction)

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

                # Rebote con restitución
                ball.velocity -= collision_normal * ball.restitution * velocity_along_normal

                # Rozamiento
                tangential_velocity = ball.velocity - \
                    collision_normal * ball.velocity.dot(collision_normal)
                if tangential_velocity.length() > 0:
                    friction_dir = tangential_velocity.normalize()
                    max_static = normal_force_magnitude * ball.static_friction
                    kinetic = tangential_velocity.length() * ball.mass / dt * ball.kinetic_friction
                    friction_force = -friction_dir * min(max_static, kinetic)
                    ball.apply_force(friction_force)
