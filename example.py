from physics.vector import Vector
from physics.objects import Ball, InclinedPlane, Rectangle
from physics.color import Color
from physics.world import World
from physics.rendering import FrameExporter

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
DT = 1 / FPS  # Delta time

world = World(SCREEN_WIDTH, SCREEN_HEIGHT, gravity=Vector(0, 500)) # Gravedad un poco más fuerte para ver efecto

# Añadir objetos
ball1 = Ball(position=Vector(100, 50), radius=20, mass=10, color=Color(255, 0, 0), restitution=0.8, static_friction=0.7, kinetic_friction=0.5)
ball1.set_label("Bola 1")
world.add_object(ball1)

ball2 = Ball(position=Vector(300, 250), radius=30, mass=15, color=Color(0, 255, 0), restitution=0.7, static_friction=0.6, kinetic_friction=0.4)
ball2.set_label("Bola 2", offset=Vector(0, 35))
world.add_object(ball2)

rect1 = Rectangle(position=Vector(350, 50), width=60, height=40, mass=20, color=Color(0, 0, 255), restitution=0.6, static_friction=0.8, kinetic_friction=0.6)
rect1.set_label("Rectángulo 1", offset=Vector(0, -30))
world.add_object(rect1)

# Añadir un plano inclinado
plane1 = InclinedPlane(start_point=Vector(100, 400), end_point=Vector(700, 500), color=Color(200, 200, 200))
world.add_object(plane1)

# Añadir otro plano inclinado para probar modularidad
plane2 = InclinedPlane(start_point=Vector(50, 250), end_point=Vector(250, 300), color=Color(150, 150, 0))
world.add_object(plane2)

frame_exporter = FrameExporter(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

NUM_FRAMES = 300  # Número de frames a simular

print("Iniciando simulación...")
for i in range(NUM_FRAMES):
    world.update(DT)
    frame_exporter.export_frame(world)
    if i % 50 == 0:
        print(f"Frame {i}/{NUM_FRAMES}")

print("Simulación terminada. Frames guardados en la carpeta 'frames/'.")
print("Para crear un GIF, puedes usar ImageMagick o FFmpeg:")
print("Ejemplo ImageMagick: convert -delay 5 -loop 0 frames/*.ppm animation.gif")
print("Ejemplo FFmpeg: ffmpeg -i frames/frame_%04d.ppm -vf 'fps=25,format=yuv420p' animation.mp4")