from models.triangle_model import TriangleModel
from services.triangle_service import TriangleService

#3
A = [6, 4]
B = [10, 12]
C = [12, 4]

triangle_model = TriangleModel(A, B, C)

triangle = TriangleService(triangle_model)

print(triangle.calculate_triangle_fill())