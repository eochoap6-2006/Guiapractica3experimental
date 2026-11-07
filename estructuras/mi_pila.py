class MiPila:
    # El último dato es el primero en salir.
    def __init__(self, capacidad=1000):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def apilar(self, dato):
        if self.cantidad == self.capacidad:
            return False
        self.datos[self.cantidad] = dato
        self.cantidad = self.cantidad + 1
        return True

    def desapilar(self):
        if self.esta_vacia():
            return None
        dato = self.datos[self.cantidad - 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return dato

    def ver_tope(self):
        if self.esta_vacia():
            return None
        return self.datos[self.cantidad - 1]

    def listar(self):
        if self.esta_vacia():
            print("Pila vacía")
            return
        for i in range(self.cantidad - 1, -1, -1):
            print(self.datos[i])

    def buscar(self, dato):
        for i in range(self.cantidad - 1, -1, -1):
            if self.datos[i] == dato:
                return i
        return -1

    def eliminar(self, dato):
        aux = MiPila(self.capacidad)
        eliminado = False
        while not self.esta_vacia():
            actual = self.desapilar()
            if actual == dato:
                eliminado = True
                break
            aux.apilar(actual)
        while not aux.esta_vacia():
            self.apilar(aux.desapilar())
        return eliminado

    def copiar(self):
        copia = MiPila(self.capacidad)
        # La copia conserva el mismo tope.
        for i in range(self.cantidad):
            copia.apilar(self.datos[i])
        return copia

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0
