from collections import deque

from enums import Direction
from vector import Vector

SNAKE_MIN_SPEED = 8.0
SNAKE_MIN_LENGTH = 5
SNAKE_SPEED_MULTIPLIER = 0.20


class Snake:
    def __init__(self, start, direction, color=None, length=1, speed=1):
        self.__direction = direction
        self.length = max(SNAKE_MIN_LENGTH, length)
        self.speed = max(SNAKE_MIN_SPEED, speed)
        self.segments = deque([start])
        self.color = color
        self.set_timer()

    def __len__(self):
        return len(self.segments)

    def __iter__(self):
        return iter(self.segments)

    @property
    def blocks(self):
        return [tuple(pos) for pos in self]

    @property
    def head(self):
        return self.segments[0]

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, value):
        if not isinstance(value, Vector):
            raise TypeError("Vector expected")
        if self.direction != -value:
            self.__direction = value

    def get_score(self):
        return self.length

    def get_speed(self):
        return self.speed

    def get_color(self):
        return self.color.value

    def set_timer(self):
        self.__timer = 1.0 / self.speed

    def extend(self, segment=None):
        if self.direction == Direction.NULL.value:
            return
        self.segments.appendleft(
            (segment or self.head) + self.direction
        )

    def suicide(self):
        return self.segments.count(self.head) > 1

    def grow(self, value=1):
        self.length += value
        self.speed += SNAKE_SPEED_MULTIPLIER * value

    def loop(self, topleft, bottomright):
        head = self.head
        if self.direction == Direction.RIGHT.value:
            new_vector = Vector((topleft[0], head[1]))
        elif self.direction == Direction.UP.value:
            new_vector = Vector((head[0], bottomright[1]))
        elif self.direction == Direction.LEFT.value:
            new_vector = Vector((bottomright[0], head[1]))
        elif self.direction == Direction.DOWN.value:
            new_vector = Vector((head[0], topleft[1]))
        self.extend(new_vector - self.direction)

    def update(self, δt, direction):
        self.__timer -= δt
        if self.__timer > 0:
            return
        self.set_timer()
        self.direction = direction
        self.extend()
        for _ in range(0, len(self) - self.length):
            self.segments.pop()
