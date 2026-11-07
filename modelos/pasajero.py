class Pasajero:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula
        self.millas = 0

    def __str__(self):
        return f"{self.nombre} ({self.cedula}) - {self.millas} millas"
