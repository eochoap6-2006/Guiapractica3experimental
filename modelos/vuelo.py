from estructuras.lista_enlazada import ListaEnlazada


class Vuelo:
    def __init__(self, id_vuelo, origen, destino, capacidad):
        self.id = id_vuelo
        self.origen = origen
        self.destino = destino
        self.capacidad = capacidad
        self.reservados = 0
        self.asientos = {}
        for numero in range(1, capacidad + 1):
            self.asientos[numero] = None
        self.itinerario = ListaEnlazada()
        self.itinerario.agregar(origen)
        self.itinerario.agregar(destino)

    def asientos_libres(self):
        return self.capacidad - self.reservados

    def esta_lleno(self):
        return self.reservados >= self.capacidad

    def primer_asiento_libre(self):
        for numero in range(1, self.capacidad + 1):
            if self.asientos[numero] is None:
                return numero
        return None

    def __str__(self):
        return (f"#{self.id} {self.origen} -> {self.destino} "
                f"({self.reservados}/{self.capacidad})")
