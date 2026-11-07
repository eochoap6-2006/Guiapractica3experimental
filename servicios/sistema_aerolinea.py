from estructuras.arbol_vuelos import ArbolVuelos
from estructuras.lista_enlazada import ListaEnlazada
from estructuras.mi_cola import MiCola
from estructuras.mi_pila import MiPila
from estructuras.red_rutas import RedRutas
from modelos.pasajero import Pasajero
from modelos.reserva import Reserva
from modelos.vuelo import Vuelo
from servicios.persistencia import ARCHIVO, cargar_todo, guardar_todo


class SistemaAerolinea:
    def __init__(self, archivo=ARCHIVO):
        self.archivo = archivo
        self.pasajeros = []
        self.vuelos = []
        self.reservas = []
        self.lista_espera = {}
        self.historial = MiPila()
        self.siguiente_reserva = 1
        self._reconstruir()
        datos = cargar_todo(archivo)
        if datos is not None:
            try:
                self._restaurar(datos)
                for accion in datos.get("historial", []):
                    if not self.historial.apilar(accion):
                        raise ValueError("El historial supera la capacidad.")
            except (KeyError, TypeError, AttributeError) as error:
                raise ValueError("Revise la estructura del archivo JSON.") from error

    def buscar_pasajero(self, cedula):
        return self.indice_pasajeros.get(cedula)

    def buscar_vuelo(self, id_vuelo):
        return self.arbol.buscar(id_vuelo)

    def buscar_reserva(self, codigo):
        for reserva in self.reservas:
            if reserva.codigo == codigo:
                return reserva
        return None

    def _reconstruir(self):
        self.indice_pasajeros = {}
        self.arbol = ArbolVuelos()
        self.red = RedRutas()
        for pasajero in self.pasajeros:
            if pasajero.cedula in self.indice_pasajeros:
                raise ValueError("Hay cédulas repetidas.")
            self.indice_pasajeros[pasajero.cedula] = pasajero
        for vuelo in self.vuelos:
            if self.arbol.buscar(vuelo.id) is not None:
                raise ValueError("Hay vuelos repetidos.")
            self.arbol.insertar(vuelo)
            vuelo.reservados = 0
            vuelo.asientos = {}
            for numero in range(1, vuelo.capacidad + 1):
                vuelo.asientos[numero] = None
            ciudades = vuelo.itinerario.a_lista()
            for i in range(len(ciudades) - 1):
                self.red.agregar_ruta(ciudades[i], ciudades[i + 1])
        codigos = set()
        pasajeros_por_vuelo = set()
        for reserva in self.reservas:
            vuelo = self.buscar_vuelo(reserva.id_vuelo)
            if vuelo is None or self.buscar_pasajero(reserva.cedula_pasajero) is None:
                raise ValueError("Una reserva tiene un pasajero o vuelo inexistente.")
            clave = (reserva.id_vuelo, reserva.cedula_pasajero)
            if reserva.codigo in codigos or clave in pasajeros_por_vuelo:
                raise ValueError("Hay reservas repetidas.")
            codigos.add(reserva.codigo)
            pasajeros_por_vuelo.add(clave)
            if reserva.asiento is None:
                reserva.asiento = vuelo.primer_asiento_libre()
            if reserva.asiento not in vuelo.asientos:
                raise ValueError("Una reserva tiene un asiento inválido.")
            if vuelo.asientos[reserva.asiento] is not None:
                raise ValueError("Hay un asiento ocupado dos veces.")
            vuelo.asientos[reserva.asiento] = reserva.codigo
            vuelo.reservados += 1

    def estado(self):
        datos = {
            "pasajeros": [], "vuelos": [], "reservas": [],
            "lista_espera": {}, "siguiente_reserva": self.siguiente_reserva,
        }
        for pasajero in self.pasajeros:
            datos["pasajeros"].append(dict(pasajero.__dict__))
        for vuelo in self.vuelos:
            datos["vuelos"].append({
                "id": vuelo.id, "origen": vuelo.origen,
                "destino": vuelo.destino, "capacidad": vuelo.capacidad,
                "reservados": vuelo.reservados,
                "itinerario": vuelo.itinerario.a_lista(),
            })
        for reserva in self.reservas:
            datos["reservas"].append(dict(reserva.__dict__))
        for id_vuelo, cola in self.lista_espera.items():
            copia = cola.copiar()
            cedulas = []
            while not copia.esta_vacia():
                cedulas.append(copia.desencolar())
            datos["lista_espera"][str(id_vuelo)] = cedulas
        return datos

    def _restaurar(self, datos):
        self.pasajeros = []
        for dato in datos.get("pasajeros", []):
            pasajero = Pasajero(dato["nombre"], dato["cedula"])
            pasajero.millas = dato.get("millas", 0)
            self.pasajeros.append(pasajero)
        self.vuelos = []
        for dato in datos.get("vuelos", []):
            vuelo = Vuelo(dato["id"], dato["origen"], dato["destino"], dato["capacidad"])
            vuelo.itinerario = ListaEnlazada()
            for ciudad in dato.get("itinerario", [vuelo.origen, vuelo.destino]):
                vuelo.itinerario.agregar(ciudad)
            self.vuelos.append(vuelo)
        self.reservas = []
        for dato in datos.get("reservas", []):
            self.reservas.append(Reserva(
                dato["codigo"], dato["cedula_pasajero"],
                dato["id_vuelo"], dato.get("asiento"),
            ))
        self.lista_espera = {}
        for id_vuelo, cedulas in datos.get("lista_espera", {}).items():
            cola = MiCola()
            for cedula in cedulas:
                if not cola.encolar(cedula):
                    raise ValueError("La lista de espera supera la capacidad.")
            self.lista_espera[int(id_vuelo)] = cola
        self.siguiente_reserva = datos.get("siguiente_reserva", 1)
        self._reconstruir()

    def guardar(self):
        datos = self.estado()
        acciones = []
        copia = self.historial.copiar()
        while not copia.esta_vacia():
            acciones.append(copia.desapilar())
        acciones.reverse()
        datos["historial"] = acciones
        guardar_todo(datos, self.archivo)

    def _registrar(self, descripcion):
        accion = {"descripcion": descripcion, "estado": self.estado()}
        if not self.historial.apilar(accion):
            raise ValueError("Historial lleno. Deshaga una acción antes de continuar.")

    def _finalizar(self, mensaje):
        try:
            self._reconstruir()
            self.guardar()
        except (OSError, ValueError):
            accion = self.historial.desapilar()
            self._restaurar(accion["estado"])
            raise
        return mensaje

    def agregar_pasajero(self, nombre, cedula):
        nombre, cedula = nombre.strip(), cedula.strip()
        if not nombre or not cedula:
            raise ValueError("Ingrese nombre y cédula.")
        if self.buscar_pasajero(cedula) is not None:
            raise ValueError("El pasajero ya existe.")
        self._registrar("agregar pasajero")
        self.pasajeros.append(Pasajero(nombre, cedula))
        return self._finalizar("Pasajero agregado")

    def modificar_pasajero(self, cedula, nombre):
        pasajero = self.buscar_pasajero(cedula)
        if pasajero is None:
            raise ValueError("El pasajero no existe.")
        if not nombre.strip():
            raise ValueError("Ingrese un nombre.")
        self._registrar("modificar pasajero")
        pasajero.nombre = nombre.strip()
        return self._finalizar("Pasajero modificado")

    def eliminar_pasajero(self, cedula):
        pasajero = self.buscar_pasajero(cedula)
        if pasajero is None:
            raise ValueError("El pasajero no existe.")
        for reserva in self.reservas:
            if reserva.cedula_pasajero == cedula:
                raise ValueError("Cancele primero las reservas del pasajero.")
        for cola in self.lista_espera.values():
            if cola.buscar(cedula) != -1:
                raise ValueError("Retire primero al pasajero de la lista de espera.")
        self._registrar("eliminar pasajero")
        self.pasajeros.remove(pasajero)
        return self._finalizar("Pasajero eliminado")

    def _validar_vuelo(self, id_vuelo, origen, destino, capacidad):
        if id_vuelo <= 0 or capacidad <= 0:
            raise ValueError("El ID y la capacidad deben ser mayores que cero.")
        if not origen or not destino or origen == destino:
            raise ValueError("Ingrese un origen y un destino diferentes.")

    def agregar_vuelo(self, id_vuelo, origen, destino, capacidad):
        origen, destino = origen.strip().title(), destino.strip().title()
        self._validar_vuelo(id_vuelo, origen, destino, capacidad)
        if self.buscar_vuelo(id_vuelo) is not None:
            raise ValueError("El vuelo ya existe.")
        self._registrar("agregar vuelo")
        self.vuelos.append(Vuelo(id_vuelo, origen, destino, capacidad))
        return self._finalizar("Vuelo agregado")

    def modificar_vuelo(self, id_vuelo, origen, destino, capacidad):
        vuelo = self.buscar_vuelo(id_vuelo)
        if vuelo is None:
            raise ValueError("El vuelo no existe.")
        origen, destino = origen.strip().title(), destino.strip().title()
        self._validar_vuelo(id_vuelo, origen, destino, capacidad)
        for reserva in self.reservas:
            if reserva.id_vuelo == id_vuelo and reserva.asiento > capacidad:
                raise ValueError("La nueva capacidad deja fuera un asiento reservado.")
        ciudades = vuelo.itinerario.a_lista()
        if origen in ciudades[1:-1] or destino in ciudades[1:-1]:
            raise ValueError("Una escala coincide con el nuevo origen o destino.")
        self._registrar("modificar vuelo")
        vuelo.origen, vuelo.destino, vuelo.capacidad = origen, destino, capacidad
        ciudades[0], ciudades[-1] = origen, destino
        vuelo.itinerario = ListaEnlazada()
        for ciudad in ciudades:
            vuelo.itinerario.agregar(ciudad)
        self._reconstruir()
        atendidos = self._procesar_espera(id_vuelo)
        mensaje = "Vuelo modificado"
        if atendidos:
            mensaje += "\n" + "\n".join(atendidos)
        return self._finalizar(mensaje)

    def eliminar_vuelo(self, id_vuelo):
        vuelo = self.buscar_vuelo(id_vuelo)
        if vuelo is None:
            raise ValueError("El vuelo no existe.")
        if vuelo.reservados > 0:
            raise ValueError("Cancele primero las reservas del vuelo.")
        cola = self.lista_espera.get(id_vuelo)
        if cola is not None and not cola.esta_vacia():
            raise ValueError("La lista de espera del vuelo no está vacía.")
        self._registrar("eliminar vuelo")
        self.vuelos.remove(vuelo)
        self.lista_espera.pop(id_vuelo, None)
        return self._finalizar("Vuelo eliminado")

    def _crear_reserva(self, cedula, vuelo, asiento=None, prefijo="R"):
        if asiento is None:
            asiento = vuelo.primer_asiento_libre()
        codigo = f"{prefijo}-{self.siguiente_reserva:04d}"
        while self.buscar_reserva(codigo) is not None:
            self.siguiente_reserva += 1
            codigo = f"{prefijo}-{self.siguiente_reserva:04d}"
        self.siguiente_reserva += 1
        reserva = Reserva(codigo, cedula, vuelo.id, asiento)
        self.reservas.append(reserva)
        vuelo.asientos[asiento] = codigo
        vuelo.reservados += 1
        return reserva

    def reservar(self, cedula, id_vuelo, asiento=None):
        vuelo = self.buscar_vuelo(id_vuelo)
        if vuelo is None or self.buscar_pasajero(cedula) is None:
            raise ValueError("El pasajero o vuelo no existe.")
        for reserva in self.reservas:
            if reserva.cedula_pasajero == cedula and reserva.id_vuelo == id_vuelo:
                raise ValueError("El pasajero ya tiene una reserva en este vuelo.")
        cola = self.lista_espera.get(id_vuelo)
        if cola is not None and cola.buscar(cedula) != -1:
            raise ValueError("El pasajero ya está en espera.")
        if asiento is not None and (asiento < 1 or asiento > vuelo.capacidad):
            raise ValueError("El asiento está fuera de la capacidad del vuelo.")
        if vuelo.esta_lleno():
            if cola is not None and cola.longitud() == cola.capacidad:
                raise ValueError("La lista de espera está llena.")
            self._registrar("agregar pasajero a espera")
            if cola is None:
                cola = MiCola()
                self.lista_espera[id_vuelo] = cola
            cola.encolar(cedula)
            return self._finalizar(f"En espera. Puesto: {cola.longitud()}")
        if asiento is not None and vuelo.asientos[asiento] is not None:
            raise ValueError("El asiento está ocupado.")
        self._registrar("crear reserva")
        reserva = self._crear_reserva(cedula, vuelo, asiento)
        return self._finalizar(f"Reserva {reserva.codigo} creada. Asiento: {reserva.asiento}")

    def _procesar_espera(self, id_vuelo):
        vuelo = self.buscar_vuelo(id_vuelo)
        cola = self.lista_espera.get(id_vuelo)
        mensajes = []
        if cola is None:
            return mensajes
        while not cola.esta_vacia() and not vuelo.esta_lleno():
            cedula = cola.desencolar()
            reserva = self._crear_reserva(cedula, vuelo, prefijo="AUTO")
            mensajes.append(f"Reserva {reserva.codigo} creada para {cedula}. "
                            f"Asiento: {reserva.asiento}")
        return mensajes

    def cancelar_reserva(self, codigo):
        reserva = self.buscar_reserva(codigo)
        if reserva is None:
            raise ValueError("La reserva no existe.")
        self._registrar("cancelar reserva")
        vuelo = self.buscar_vuelo(reserva.id_vuelo)
        self.reservas.remove(reserva)
        vuelo.asientos[reserva.asiento] = None
        vuelo.reservados -= 1
        atendidos = self._procesar_espera(vuelo.id)
        mensaje = "Reserva cancelada"
        if atendidos:
            mensaje += "\n" + "\n".join(atendidos)
        return self._finalizar(mensaje)

    def retirar_espera(self, id_vuelo, cedula):
        cola = self.lista_espera.get(id_vuelo)
        if cola is None or cola.buscar(cedula) == -1:
            raise ValueError("El pasajero no está en esa lista de espera.")
        self._registrar("retirar pasajero de espera")
        cola.eliminar(cedula)
        return self._finalizar("Pasajero retirado de la lista de espera")

    def agregar_escala(self, id_vuelo, posicion, ciudad):
        vuelo = self.buscar_vuelo(id_vuelo)
        if vuelo is None:
            raise ValueError("El vuelo no existe.")
        ciudad = ciudad.strip().title()
        if not ciudad or ciudad in vuelo.itinerario.a_lista():
            raise ValueError("Ingrese una ciudad que no esté en el itinerario.")
        if posicion < 1 or posicion >= vuelo.itinerario.longitud():
            raise ValueError("La escala debe ir entre el origen y el destino.")
        self._registrar("agregar escala")
        vuelo.itinerario.insertar(posicion, ciudad)
        return self._finalizar("Escala agregada")

    def eliminar_escala(self, id_vuelo, posicion):
        vuelo = self.buscar_vuelo(id_vuelo)
        if vuelo is None:
            raise ValueError("El vuelo no existe.")
        if posicion < 1 or posicion >= vuelo.itinerario.longitud() - 1:
            raise ValueError("Solo puede eliminar una escala intermedia.")
        self._registrar("eliminar escala")
        vuelo.itinerario.eliminar(posicion)
        return self._finalizar("Escala eliminada")

    def deshacer(self):
        if self.historial.esta_vacia():
            return "Nada que deshacer"
        actual = self.estado()
        accion = self.historial.desapilar()
        self._restaurar(accion["estado"])
        try:
            self.guardar()
        except OSError:
            self._restaurar(actual)
            self.historial.apilar(accion)
            raise
        return "Deshecho: " + accion["descripcion"]
