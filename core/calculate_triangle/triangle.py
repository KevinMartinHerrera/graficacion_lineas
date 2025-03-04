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
        self.slope = 0
        self.direction = 0

    def __calculate_slope(self, point_one, point_two):
        slope = CalculateSlope(point_one, point_two).slope()
        return slope
    
    def __calculate_direction(self, point_one, point_two):
        direction = CalculateLineDirection(point_one, point_two).line_direction()
        return direction
        
    def __calculate_line(self, point_one, point_two):
        line_model = LineModel(point_one, point_two)
        slope = self.__calculate_slope(line_model.point_a, line_model.point_b)
        direction = self.__calculate_direction(line_model.point_a, line_model.point_b)
        points = DDALinea(line_model.point_a, line_model.point_b, slope, direction).calculate_line()
        points = self.__convert_coordinates(points)
        line_properties = {
                "direccion": direction,
                "pendiente": slope,
                "coordenadas": points
            }
        
        return line_properties        
        
    def calculate_triangle(self):
        self.triangle_point_ab = self.__calculate_line(self.triangle.point_a, self.triangle.point_b)
        self.triangle_point_bc = self.__calculate_line(self.triangle.point_b, self.triangle.point_c)
        self.triangle_point_ca = self.__calculate_line(self.triangle.point_c, self.triangle.point_a)
        
        triangle = [self.triangle_point_ab, self.triangle_point_bc, self.triangle_point_ca]
        return triangle
    
    def __convert_coordinates(self, coordinates):
        coordinates_tuple = []
        if isinstance(coordinates, list):
            for coordinate in coordinates:
                coordinates_tuple.append(tuple(coordinate))
        coordinates_tuple = tuple(coordinates_tuple)
        return coordinates_tuple
    
    def calculate_triangle_fill(self):
        # Cálculo de bordes
        self.ab_points = self._calculate_edge(self.triangle.point_a, self.triangle.point_b)
        self.bc_points = self._calculate_edge(self.triangle.point_b, self.triangle.point_c)
        
        # Relleno
        fill_lines = []
        for point in self.bc_points["coordenadas"][1:-1]:
            fill_line = self._calculate_edge(self.triangle.point_a, point)
            fill_lines.append(fill_line)
        
        return {
            "AB": self.ab_points,
            "BC": self.bc_points,
            "AC": fill_lines
        }
    def _calculate_edge(self, start, end):
        direction = CalculateLineDirection(start, end).line_direction()
        slope = CalculateSlope(start, end).slope()
        points = DDALinea(start, end, slope, direction).calculate_line()
        
        return {
            "direccion": direction,
            "pendiente": slope,
            "coordenadas": points
        }