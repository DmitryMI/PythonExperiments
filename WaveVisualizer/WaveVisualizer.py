from PIL import Image, ImageDraw
import math

FIELD_WIDTH = 100
FIELD_HEIGHT = 300

# Dimensions of a pixel in meters
PIXEL_SCALE = 1

# Wave speed in meters per second
WAVE_SPEED = 300

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def distance_sqr(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        dz = self.z - point.z
        dsqr = dx * dx + dy * dy + dz * dz
        return dsqr

    def distance(self, point):
        dsqr = self.distance_sqr(point)
        return math.sqrt(dsqr)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


class WaveSource:
    def __init__(self, location: Vector3, amplitude: float, frequency: float, phase_shift: float):
        self.location = location
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift

    def wave(self, time: float):
        return self.amplitude * math.sin(2 * math.pi * self.frequency * time + self.phase_shift)


class SimulationField:
    def __init__(self, wave_source_list, width, height, precision):
        self.wave_sources = []
        for src in wave_source_list:
            self.wave_sources.append(src)

        self.width = width
        self.height = height
        self.precision = precision

    def snapshot_location(self, time, x, y):
        value = 0.0
        point = Vector3(x, y, 0)
        for src in self.wave_sources:
            time_to_point = src.location.distance(point) / WAVE_SPEED
            if time - time_to_point < 0:
                continue
            src_value = src.wave(time + time_to_point)
            value += src_value
        return value


    @staticmethod
    def sine_to_greyscale(value, max_absolute_amplitude=1.0):
        if value < -max_absolute_amplitude:
            value = max_absolute_amplitude
        if value > max_absolute_amplitude:
            value = max_absolute_amplitude

        k = 255 / (2 * max_absolute_amplitude)
        b = 255 / 2
        return int(k * value + b)


    @staticmethod
    def amplitude_to_greyscale(value, max_absolute_amplitude=1.0):
        value = math.fabs(value)

        if value > max_absolute_amplitude:
            value = max_absolute_amplitude

        k = 255 / max_absolute_amplitude
        return int(k * value)


    def draw_snapshot(self, time):
        pixel_width = int(self.width / self.precision)
        pixel_height = int(self.height / self.precision)

        image = Image.new('L', (pixel_width, pixel_height), color = 'black')        

        for x in range(pixel_width):
            for y in range(pixel_height):
                location_x = x * self.precision
                location_y = y * self.precision
                value = self.snapshot_location(time, location_x, location_y)
                #color = SimulationField.amplitude_to_color(value)
                
                color = SimulationField.amplitude_to_greyscale(value, 10.0) 
                image.putpixel((x, y), color)
            print(f"Row {x} finished")

        image.show()

wave_sources = []
center_x = FIELD_WIDTH / 2
spacing = 2
count = 8
phase_shift = math.radians(-20)

initial_phase = 0.0
for i in range(count):
    x = center_x + spacing * (i - count / 2)
    src = WaveSource(Vector3(x, 50, 0), 1.0, 100.0, initial_phase + i * phase_shift)
    print(f"Created source on poisiton {str(src.location)}")
    wave_sources.append(src)

simulator = SimulationField(wave_sources, FIELD_WIDTH, FIELD_HEIGHT, PIXEL_SCALE)
time = 10.0

simulator.draw_snapshot(time)
        
         