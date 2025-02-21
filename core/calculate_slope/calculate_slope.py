class CalculateSlope:
    def __init__(self, A, B):
        self._x1 = A[0]
        self._y1 = A[1]
        self._x2 = B[0]
        self._y2 = B[1]
        
    def slope(self):
        dy = self._y2 - self._y1
        dx = self._x2 - self._x1
        if dy == 0:
            return 0
        if dx == 0:
            return None
        _slope = round(dy / dx, 4)
        return _slope