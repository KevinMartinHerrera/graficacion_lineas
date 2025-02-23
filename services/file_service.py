import csv

class FileService:
    @staticmethod
    def export_points_to_csv(file_path, points):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["X", "Y"])
            for point in points:
                writer.writerow([round(point[0], 2), round(point[1], 2)])