from core.calculate_triangle.triangle import Triangle
from models.triangle_model import TriangleModel
from core.calculate_line_direction.calculate_line_direction import CalculateLineDirection
from core.calculate_slope.calculate_slope import CalculateSlope
from services.line_service import LineService
#3
A = [6, 4]
B = [10, 12]
C = [12, 4]

triangle_model = TriangleModel(A, B, C)

triangle = Triangle(triangle_model).calculate_triangle()

slope_ab = CalculateSlope(triangle_model.point_a, triangle_model.point_b).slope()
slope_bc = CalculateSlope(triangle_model.point_b, triangle_model.point_c).slope()
slope_ca = CalculateSlope(triangle_model.point_c, triangle_model.point_a).slope()

direction_ab = CalculateLineDirection(triangle_model.point_a, triangle_model.point_b).line_direction()
direction_bc = CalculateLineDirection(triangle_model.point_b, triangle_model.point_c).line_direction()
direction_ca = CalculateLineDirection(triangle_model.point_c, triangle_model.point_a).line_direction()

print(f"Pendiente AB: {slope_ab} con direccion: {direction_ab}")
print(f"Pendiente BC: {slope_bc} con direccion: {direction_bc}")
print(f"Pendiente CA: {slope_ca} con direccion: {direction_ca}")

print(f"Pendiente AB: {triangle} con direccion: {direction_ab}")