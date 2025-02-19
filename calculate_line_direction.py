class CalculateLineDirection:
    def __init__(self, A, B):
        self._x1 = A[0]
        self._y1 = A[1]
        self._x2 = B[0]
        self._y2 = B[1]

    def line_direction(self):
        #Izquierda a Derecha
        if self._x1 < self._x2: #_x1 menor a _x2 
            #Abajo hacia Arriba
            if self._y1 < self._y2: #y _y1 menor a _y2
                return 1
            #Arriba hacia Abajo
            elif self._y1 > self._y2: #y _y1 mayor a _y2
                return 2
            #Linea recta
            elif self._y1 == self._y2:
                return 3
        #Derecha a Izquiera
        elif self._x1 > self._x2: #_x1 mayor a _x2 
            #Abajo hacia Arriba
            if self._y1 < self._y2: #y _y1 menor a _y2
                return 4
            #Arriba hacia Abajo
            elif self._y1 > self._y2: #y _y1 mayor a _y2
                return 5
            #Linea recta
            elif self._y1 == self._y2:
                return 6
        #Linea recta
        elif self._x1 == self._x2: #_x1 mayor a _x2 
            #Abajo hacia Arriba
            if self._y1 < self._y2: #y _y1 menor a _y2
                return 7
            #Arriba hacia Abajo
            elif self._y1 > self._y2: #y _y1 mayor a _y2
                return 8
        