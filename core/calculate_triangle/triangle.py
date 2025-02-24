from core.dda_line.dda_line import DDALinea
from core.calculate_line_direction.calculate_line_direction import CalculateLineDirection
from core.calculate_slope.calculate_slope import CalculateSlope
from services.line_service import LineService
from models.line_model import LineModel

class Triangle ():
    def __init__(self, triangle):
        self.triangle = triangle
        self.triangle_point_ab = []
        self.triangle_point_bc = []
        self.triangle_point_ca = []
        
    def __calculate_line(self, point_one, point_two):
        line_model = LineModel(point_one, point_two)
        line = LineService(line_model).calculate_line_properties()
        return line
        
    def __calculate_slope(point_one, point_two):
        slope = CalculateSlope(point_one, point_two).slope()
        return slope
    
    def __calculate_direction(point_one, point_two):
        direction = CalculateLineDirection(point_one, point_two).line_direction()
        return direction
        
    def calculate_triangle(self):
        self.triangle_point_ab = self.__calculate_line(self.triangle.point_a, self.triangle.point_b)
        self.triangle_point_bc = self.__calculate_line(self.triangle.point_b, self.triangle.point_c)
        self.triangle_point_ca = self.__calculate_line(self.triangle.point_c, self.triangle.point_a)
        
        triangle = [self.triangle_point_ab, self.triangle_point_bc, self.triangle_point_ca]
        return triangle
    
    def calculate_triangle_fill(self):
        pass