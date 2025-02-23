from services.line_service import LineService
from models.line_model import LineModel

#3
A = [10, 40]
B = [20, 25]

line_model = LineModel(A, B)

line_data = LineService(line_model).calculate_line_properties()

print(line_data)