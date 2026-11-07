class MiCola:

    # CREAR
    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    # ENCOLAR
    def encolar(self, pasajero):
        if self.cantidad == self.capacidad:
            print("La cola está llena")
            return False
        if self.buscar(pasajero.cedula) != -1:
            print(pasajero.cedula, "ya existe")
            return False
        self.datos[self.cantidad] = pasajero
        self.cantidad = self.cantidad + 1
        return True

    # LISTAR
    def listar(self):
        if self.cantidad == 0:
            print("Cola vacía")
            return
        for i in range(self.cantidad):
            if i == 0:
                print(f"[{i}] {self.datos[i]} - FRENTE")
            elif i == self.cantidad - 1:
                print(f"[{i}] {self.datos[i]} - FINAL")
            else:
                print(f"[{i}] {self.datos[i]}")

    # DESENCOLAR
    def desencolar(self):
        if self.cantidad == 0:
            return None
        pasajero = self.datos[0]
        for i in range(self.cantidad - 1):
            self.datos[i] = self.datos[i + 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return pasajero

    # VER FRENTE
    def ver_frente(self):
        if self.cantidad == 0:
            return None
        return self.datos[0]

    # BUSCAR
    def buscar(self, cedula):
        for i in range(self.cantidad):
            if self.datos[i].cedula == cedula:
                return i
        return -1

    # MODIFICAR
    def modificar(self, cedula, nuevo_nombre, nueva_edad):
        pos = self.buscar(cedula)
        if pos == -1:
            print(cedula, "no existe")
            return False
        if not nuevo_nombre.strip() or nueva_edad < 0:
            print("Nombre o edad no válidos")
            return False
        self.datos[pos].nombre = nuevo_nombre
        self.datos[pos].edad = nueva_edad
        return True

    # ELIMINAR POR CÉDULA
    def eliminar_por_cedula(self, cedula):
        cantidad = self.cantidad
        eliminado = False
        for i in range(cantidad):
            pasajero = self.desencolar()
            if pasajero.cedula == cedula:
                eliminado = True
            else:
                self.encolar(pasajero)
        if not eliminado:
            print(cedula, "no existe")
        return eliminado

    # COPIAR
    def copiar(self):
        nueva = MiCola(self.capacidad)
        for i in range(self.cantidad):
            nueva.encolar(self.datos[i])
        return nueva

    # LONGITUD
    def longitud(self):
        return self.cantidad

    # ESTÁ VACÍA
    def esta_vacia(self):
        return self.cantidad == 0
