class MiCola:
    # El primer dato es el primero en salir.
    def __init__(self, capacidad=1000):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def encolar(self, dato):
        if self.cantidad == self.capacidad:
            return False
        self.datos[self.cantidad] = dato
        self.cantidad = self.cantidad + 1
        return True

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.datos[0]
        for i in range(self.cantidad - 1):
            self.datos[i] = self.datos[i + 1]
        self.cantidad = self.cantidad - 1
        self.datos[self.cantidad] = None
        return dato

    def ver_frente(self):
        if self.esta_vacia():
            return None
        return self.datos[0]

    def listar(self):
        if self.esta_vacia():
            print("Cola vacía")
            return
        for i in range(self.cantidad):
            print(self.datos[i])

    def buscar(self, dato):
        for i in range(self.cantidad):
            if self.datos[i] == dato:
                return i
        return -1

    def eliminar(self, dato):
        cantidad = self.cantidad
        eliminado = False
        for i in range(cantidad):
            actual = self.desencolar()
            if actual == dato and not eliminado:
                eliminado = True
            else:
                self.encolar(actual)
        return eliminado

    def copiar(self):
        copia = MiCola(self.capacidad)
        for i in range(self.cantidad):
            copia.encolar(self.datos[i])
        return copia

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0
