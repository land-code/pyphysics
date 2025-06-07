import os
from PIL import Image, ImageDraw

from .color import Color

class FrameExporter:
    def __init__(self, output_dir="frames", width=800, height=600, bg_color=Color(0, 0, 0)):
        self.output_dir = output_dir
        self.width = width
        self.height = height
        self.bg_color = bg_color
        os.makedirs(self.output_dir, exist_ok=True)
        self.frame_count = 0

    def export_frame(self, world):
        """Exporta a un archivo .ppm"""
        image = Image.new("RGB", (self.width, self.height),
                          self.bg_color.to_rgb())
        draw = ImageDraw.Draw(image)
        world.draw(draw)

        filename = os.path.join(
            self.output_dir, f"frame_{self.frame_count:04d}.ppm")
        image.save(filename)
        self.frame_count += 1
        print(f"Exported {filename}")

    def get_frame_image(self, world):
        """Devuelve un objeto PIL. Image con el frame renderizado en memoria (para renderizar en js)"""
        image = Image.new("RGB", (self.width, self.height),
                          self.bg_color.to_rgb())
        draw = ImageDraw.Draw(image)
        world.draw(draw)
        self.frame_count += 1
        return image
