class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cantidad = 0

    def agregar(self, dato):
        self.insertar(self.cantidad, dato)

    def insertar(self, posicion, dato):
        if posicion < 0 or posicion > self.cantidad:
            return False
        nuevo = Nodo(dato)
        if posicion == 0:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            for i in range(posicion - 1):
                actual = actual.siguiente
            nuevo.siguiente = actual.siguiente
            actual.siguiente = nuevo
        self.cantidad += 1
        return True

    def eliminar(self, posicion):
        if posicion < 0 or posicion >= self.cantidad:
            return None
        if posicion == 0:
            dato = self.cabeza.dato
            self.cabeza = self.cabeza.siguiente
        else:
            actual = self.cabeza
            for i in range(posicion - 1):
                actual = actual.siguiente
            dato = actual.siguiente.dato
            actual.siguiente = actual.siguiente.siguiente
        self.cantidad -= 1
        return dato

    def a_lista(self):
        datos = []
        actual = self.cabeza
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos

    def longitud(self):
        return self.cantidad
