from estructuras.mi_cola import MiCola


class RedRutas:
    def __init__(self):
        self.ady = {}

    def agregar_ruta(self, ciudad_a, ciudad_b):
        self.ady.setdefault(ciudad_a, set()).add(ciudad_b)
        self.ady.setdefault(ciudad_b, set()).add(ciudad_a)

    def camino_mas_corto(self, origen, destino):
        if origen not in self.ady or destino not in self.ady:
            return None
        if origen == destino:
            return [origen]
        anterior = {origen: None}
        cola = MiCola(len(self.ady))
        cola.encolar(origen)
        while not cola.esta_vacia():
            actual = cola.desencolar()
            for vecino in sorted(self.ady[actual]):
                if vecino not in anterior:
                    anterior[vecino] = actual
                    if vecino == destino:
                        camino = []
                        ciudad = destino
                        while ciudad is not None:
                            camino.append(ciudad)
                            ciudad = anterior[ciudad]
                        camino.reverse()
                        return camino
                    cola.encolar(vecino)
        return None
