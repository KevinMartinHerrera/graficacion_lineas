from core.calculate_line_direction.calculate_line_direction import CalculateLineDirection
from core.calculate_slope.calculate_slope import CalculateSlope
from core.dda_line.dda_line import DDALinea

class LineService:
    def __init__(self, line):
        self.line = line

    def calculate_line_properties(self):
        direction = CalculateLineDirection(self.line.point_a, self.line.point_b).line_direction()
        slope = CalculateSlope(self.line.point_a, self.line.point_b).slope()
        points = DDALinea(self.line.point_a, self.line.point_b, slope, direction).calculate_line()
        return direction, slope, points