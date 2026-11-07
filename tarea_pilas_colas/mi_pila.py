class MiPila:

    # CREAR
    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    # APILAR
    def apilar(self, pasajero):
        if self.cantidad == self.capacidad:
            print("La pila está llena")
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
            print("Pila vacía")
            return
        for i in range(self.cantidad - 1, -1, -1):
            if i == self.cantidad - 1:
                print(f"[{i}] {self.datos[i]} - TOPE")
            elif i == 0:
                print(f"[{i}] {self.datos[i]} - FONDO")
            else:
                print(f"[{i}] {self.datos[i]}")

    # DESAPILAR
    def desapilar(self):
        if self.cantidad == 0:
            return None
        pasajero = self.datos[self.cantidad - 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return pasajero

    # VER TOPE
    def ver_tope(self):
        if self.cantidad == 0:
            return None
        return self.datos[self.cantidad - 1]

    # BUSCAR
    def buscar(self, cedula):
        for i in range(self.cantidad - 1, -1, -1):
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
        aux = MiPila(self.capacidad)
        eliminado = False
        while not self.esta_vacia():
            pasajero = self.desapilar()
            if pasajero.cedula == cedula:
                eliminado = True
                break
            aux.apilar(pasajero)
        while not aux.esta_vacia():
            self.apilar(aux.desapilar())
        if not eliminado:
            print(cedula, "no existe")
        return eliminado

    # COPIAR
    def copiar(self):
        nueva = MiPila(self.capacidad)
        for i in range(self.cantidad):
            nueva.apilar(self.datos[i])
        return nueva

    # LONGITUD
    def longitud(self):
        return self.cantidad

    # ESTÁ VACÍA
    def esta_vacia(self):
        return self.cantidad == 0

    # FILTRAR MAYORES DE EDAD
    def filtrar_mayores_de_edad(self):
        aux = MiPila(self.capacidad)
        resultado = MiPila(self.capacidad)
        for i in range(self.cantidad - 1, -1, -1):
            if self.datos[i].es_mayor_de_edad():
                aux.apilar(self.datos[i])
        while not aux.esta_vacia():
            resultado.apilar(aux.desapilar())
        return resultado

    # NOMBRES EN MAYÚSCULAS
    def nombres_en_mayusculas(self):
        resultado = [None] * self.cantidad
        posicion = 0
        for i in range(self.cantidad - 1, -1, -1):
            resultado[posicion] = self.datos[i].nombre.upper()
            posicion = posicion + 1
        return resultado
