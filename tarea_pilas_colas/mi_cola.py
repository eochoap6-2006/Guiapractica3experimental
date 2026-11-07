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
        if self.buscar(pasajero.numero) != -1:
            print(pasajero.numero, "ya existe")
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
    def buscar(self, numero):
        for i in range(self.cantidad):
            if self.datos[i].numero == numero:
                return i
        return -1

    # MODIFICAR
    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        pos = self.buscar(numero)
        if pos == -1:
            print(numero, "no existe")
            return False
        if not nuevo_destino.strip() or not nuevo_asiento.strip():
            print("Destino o asiento no válidos")
            return False
        self.datos[pos].destino = nuevo_destino.strip()
        self.datos[pos].asiento = nuevo_asiento.strip().upper()
        return True

    # ELIMINAR POR NÚMERO
    def eliminar_por_numero(self, numero):
        cantidad = self.cantidad
        eliminado = False
        for i in range(cantidad):
            pasajero = self.desencolar()
            if pasajero.numero == numero:
                eliminado = True
            else:
                self.encolar(pasajero)
        if not eliminado:
            print(numero, "no existe")
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

    # FILTRAR MAYORES DE EDAD
    def filtrar_mayores_de_edad(self):
        resultado = MiCola(self.capacidad)
        for i in range(self.cantidad):
            if self.datos[i].es_mayor_de_edad():
                resultado.encolar(self.datos[i])
        return resultado

    # NOMBRES EN MAYÚSCULAS
    def nombres_en_mayusculas(self):
        resultado = [None] * self.cantidad
        for i in range(self.cantidad):
            resultado[i] = self.datos[i].nombre.upper()
        return resultado
