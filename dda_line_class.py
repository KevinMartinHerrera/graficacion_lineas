class LineaDDA:
    def __init__(self, A, B, slope, direction):
        self._slope = slope
        self._direction = direction
        self._x1 = A[0]
        self._y1 = A[1]
        self._x2 = B[0]
        self._y2 = B[1]
        self._is_negative = False
        
    def __calculate_line_left_right_down_up(self):  #Derecha a Izquierda, Abajo hacia Arriba
        points = []
        y = self._y1
        x = self._x1
        if self._slope < 1: #Pendiente menor a 1
            while x < self._x2 + 1:
                points.append([round(x, 2), round(y, 2)])
                y = y + self._slope
                x += 1
        elif self._slope == 1: #Pendiente igual a 1
            while x < self._x2 + 1:
                points.append([round(x, 2), round(y, 2)])
                y += 1
                x += 1
        elif self._slope > 1:#Pendiente mayor a 1
            while y < self._y2 + 1:
                points.append([round(x, 2), round(y, 2)])
                x = x + (1 / self._slope)
                y += 1
        return points
    
    def __calculate_negative_line_left_right_up_down(self): #Izquierda a Derecha, Arriba a Abajo
        _slope = self._slope * - 1 #Valor absoluto de la pendiente
        points = []
        y = self._y1
        x = self._x1
        if _slope < 1: #Pendiente menor a 1
            while x < self._x2 + 1:
                points.append([round(x, 2), round(y, 2)])
                y = y - _slope
                x += 1
        elif _slope == 1: #Pendiente igual a 1
            while x < self._x2 + 1:
                points.append([round(x, 2), round(y, 2)])
                y -= 1
                x += 1
        elif _slope > 1:#Pendiente mayor a 1
            while y > self._y2 - 1:
                points.append([round(x, 2), round(y, 2)])
                x = x + (1 / _slope)
                y -= 1
        return points
    
    def __calculate_negative_line_right_left_down_up(self): #Derecha a Izquierda, Abajo a Arriba
        _slope = self._slope * - 1 #Valor absoluto de la pendiente
        points = []
        y = self._y1
        x = self._x1
        if _slope < 1: 
            while x > self._x2 - 1:
                points.append([round(x, 2), round(y, 2)])
                y = y + _slope
                x -= 1
        elif _slope == 1:
            while x > self._x2 - 1:
                points.append([round(x, 2), round(y, 2)])
                y += 1
                x -= 1
        elif _slope > 1:
            while y < self._y2 + 1:
                points.append([round(x, 2), round(y, 2)])
                x = x - (1 / _slope)
                y += 1
        return points  
    
    def __calculate_line_right_left_up_down(self):
        points = []
        y = self._y1
        x = self._x1
        if self._slope < 1: 
            while x > self._x2 - 1:
                points.append([round(x, 2), round(y, 2)])
                y = y - self._slope
                x -= 1
        elif self._slope == 1:
            while x > self._x2 - 1:
                points.append([round(x, 2), round(y, 2)])
                y -= 1
                x -= 1
        elif self._slope > 1:
            while y > self._y2 - 1:
                points.append([round(x, 2), round(y, 2)])
                x = x - (1 / self._slope)
                y -= 1
        return points
    
    def __slope_equal_zero(self):
        points = []
        x = self._x1
        if self._direction == 3:
            while x < self._x2 + 1:
                points.append([round(x, 2), round(self._y1, 2)])
                x += 1
        elif self._direction == 6:
            while x > self._x2 - 1:
                points.append([round(x, 2), round(self._y1, 2)])
                x -= 1
        return points 

    def __slope_equal_none(self):
        points = []
        y = self._y1
        if self._direction == 7:
            while y < self._y2 + 1:
                points.append([round(self._x1, 2), round(y, 2)])
                y += 1
        elif self._direction == 8:
            while y > self._y2 - 1:
                points.append([round(self._x1, 2), round(y, 2)])
                y -= 1
        return points    
    
    def calculate_line(self):
        if self._direction == 1 and self._slope > 0: #Izquierda a Derecha, Abajo a Arriba con pendiente positiva o negativa
            print("Izquierda a Derecha, Abajo a Arriba")
            points = self.__calculate_line_left_right_down_up()
            return points
        if self._direction == 2 and self._slope < 0: #Izquierda a Derecha, Arriba a ABajo
            print("Izquierda a Derecha, Arriba a Abajo")
            points = self.__calculate_negative_line_left_right_up_down()
            return points
        if self._direction == 4 and self._slope < 0:
            print("Derecha a Izquierda, Abajo a Arriba")
            points = self.__calculate_negative_line_right_left_down_up()
            return points
        elif self._direction == 5 and self._slope > 0:#Derecha a Izquierda, Arriba a Abajo
            print("Derecha a Izquierda, Arriba a Abajo")
            points = self.__calculate_line_right_left_up_down()
            return points
        elif self._direction == 3 or self._direction == 6:
            print("Solo Derecha a Izquierda o viceverza")
            points = self.__slope_equal_zero()
            return points
        elif self._direction == 7 or self._direction == 8:
            print("Solo Arriba a Abajo o viceverza")
            points = self.__slope_equal_none()
            return points
        