class Reserva:
    def __init__(self, codigo, cedula_pasajero, id_vuelo, asiento=None):
        self.codigo = codigo
        self.cedula_pasajero = cedula_pasajero
        self.id_vuelo = id_vuelo
        self.asiento = asiento

    def __str__(self):
        return (f"Reserva {self.codigo}: pasajero {self.cedula_pasajero} "
                f"en vuelo #{self.id_vuelo}, asiento {self.asiento}")
