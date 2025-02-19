from calculate_slope import CalculateSlope
from calculate_line_direction import CalculateLineDirection
from dda_line_class import LineaDDA
#3
A = [10, 40]
B = [20, 25]
slope = CalculateSlope(A, B)
direction = CalculateLineDirection(A,B)
_slope = slope.slope()
_direction = direction.line_direction()
line = LineaDDA(A, B, _slope, _direction)
print(f"Pendiente de A{A} a B{B}: {slope.slope()} y direccion: {_direction}")
print(f"con la linea {line.calculate_line()}") 
