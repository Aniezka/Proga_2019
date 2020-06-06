from abc import ABC, abstractmethod
import numpy as np


class Shape(ABC):
    @abstractmethod
    def get_volume(self):
        pass


class Pyramid(Shape):
    def __init__(self, s: float, h: float):
        if s <= 0 or h <= 0:
            raise ValueError
        self.s = s
        self.h = h

    def get_volume(self):
        return 1/3*self.s*self.h


class SolidOfRevolution(Shape):
    pass


class Cylinder(SolidOfRevolution):
    def __init__(self, r: float, h: float):
        if r <= 0 or h <= 0:
            raise ValueError
        self.r = r
        self.h = h

    def get_volume(self) -> float:
        return np.pi*self.r**2*self.h


class Ball(SolidOfRevolution):
    def __init__(self, r: float):
        if r <= 0:
            raise ValueError
        self.r = r

    def get_volume(self) -> float:
        return 4/3*np.pi*self.r**3


class Box(Shape):
    shapes = []

    def __init__(self, max_volume: float):
        if max_volume < 0:
            raise ValueError
        self.max_volume = max_volume
        self.curr_vol = 0

    def add(self, shape: Shape):
        if self.curr_vol + shape.get_volume() <= self.max_volume:
            self.shapes.append(shape)
            self.curr_vol += shape.get_volume()
        else:
            raise ValueError

    def get_volume(self):
        return self.curr_vol
