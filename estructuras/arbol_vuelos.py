class NodoArbol:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.izq = None
        self.der = None


class ArbolVuelos:
    def __init__(self):
        self.raiz = None

    def insertar(self, vuelo):
        self.raiz = self._insertar(self.raiz, vuelo)

    def _insertar(self, nodo, vuelo):
        if nodo is None:
            return NodoArbol(vuelo)
        if vuelo.id < nodo.vuelo.id:
            nodo.izq = self._insertar(nodo.izq, vuelo)
        elif vuelo.id > nodo.vuelo.id:
            nodo.der = self._insertar(nodo.der, vuelo)
        return nodo

    def buscar(self, id_vuelo):
        actual = self.raiz
        while actual is not None:
            if id_vuelo == actual.vuelo.id:
                return actual.vuelo
            if id_vuelo < actual.vuelo.id:
                actual = actual.izq
            else:
                actual = actual.der
        return None
