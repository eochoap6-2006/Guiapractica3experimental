from servicios.sistema_aerolinea import SistemaAerolinea


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Ingrese un dato.")


def leer_entero(mensaje, minimo=1, opcional=False):
    while True:
        texto = input(mensaje).strip()
        if opcional and texto == "":
            return None
        try:
            numero = int(texto)
            if numero >= minimo:
                return numero
            print(f"Ingrese un número desde {minimo}.")
        except ValueError:
            print("Debe ser un número entero.")


def ejecutar(funcion, *args):
    try:
        print(funcion(*args))
    except ValueError as error:
        print(error)
    except OSError:
        print("No se pudo guardar. Revise el archivo de datos.")


def agregar_pasajero(sistema):
    nombre = leer_texto("Nombre: ")
    cedula = leer_texto("Cédula: ")
    ejecutar(sistema.agregar_pasajero, nombre, cedula)


def agregar_vuelo(sistema):
    id_vuelo = leer_entero("ID vuelo: ")
    origen = leer_texto("Origen: ")
    destino = leer_texto("Destino: ")
    capacidad = leer_entero("Capacidad: ")
    ejecutar(sistema.agregar_vuelo, id_vuelo, origen, destino, capacidad)


def reservar(sistema):
    cedula = leer_texto("Cédula pasajero: ")
    id_vuelo = leer_entero("ID vuelo: ")
    vuelo = sistema.buscar_vuelo(id_vuelo)
    if vuelo is None or sistema.buscar_pasajero(cedula) is None:
        print("El pasajero o vuelo no existe.")
        return
    asiento = None
    if not vuelo.esta_lleno():
        print(f"Asientos libres: {vuelo.asientos_libres()}")
        asiento = leer_entero("Asiento (Enter para asignar): ", opcional=True)
    ejecutar(sistema.reservar, cedula, id_vuelo, asiento)


def buscar_vuelo(sistema):
    vuelo = sistema.buscar_vuelo(leer_entero("ID a buscar: "))
    print(vuelo if vuelo is not None else "El vuelo no existe.")


def mostrar_reservas(sistema):
    if not sistema.reservas:
        print("Sin reservas")
    for reserva in sistema.reservas:
        print(reserva)


def menu_pasajeros(sistema):
    while True:
        print("\nPASAJEROS")
        print("1. Agregar")
        print("2. Listar")
        print("3. Buscar")
        print("4. Modificar nombre")
        print("5. Eliminar")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            agregar_pasajero(sistema)
        elif opcion == "2":
            if not sistema.pasajeros:
                print("Sin pasajeros")
            for pasajero in sistema.pasajeros:
                print(pasajero)
        elif opcion == "3":
            pasajero = sistema.buscar_pasajero(leer_texto("Cédula: "))
            print(pasajero if pasajero is not None else "El pasajero no existe.")
        elif opcion == "4":
            cedula = leer_texto("Cédula: ")
            nombre = leer_texto("Nuevo nombre: ")
            ejecutar(sistema.modificar_pasajero, cedula, nombre)
        elif opcion == "5":
            ejecutar(sistema.eliminar_pasajero, leer_texto("Cédula: "))
        elif opcion == "0":
            return
        else:
            print("Opción no válida")


def menu_vuelos(sistema):
    while True:
        print("\nVUELOS")
        print("1. Agregar")
        print("2. Listar")
        print("3. Buscar")
        print("4. Modificar")
        print("5. Eliminar")
        print("6. Ver asientos")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            agregar_vuelo(sistema)
        elif opcion == "2":
            if not sistema.vuelos:
                print("Sin vuelos")
            for vuelo in sistema.vuelos:
                print(vuelo)
        elif opcion == "3":
            buscar_vuelo(sistema)
        elif opcion == "4":
            id_vuelo = leer_entero("ID vuelo: ")
            origen = leer_texto("Nuevo origen: ")
            destino = leer_texto("Nuevo destino: ")
            capacidad = leer_entero("Nueva capacidad: ")
            ejecutar(sistema.modificar_vuelo, id_vuelo, origen, destino, capacidad)
        elif opcion == "5":
            ejecutar(sistema.eliminar_vuelo, leer_entero("ID vuelo: "))
        elif opcion == "6":
            vuelo = sistema.buscar_vuelo(leer_entero("ID vuelo: "))
            if vuelo is None:
                print("El vuelo no existe.")
                continue
            for numero, codigo in vuelo.asientos.items():
                estado = "Libre" if codigo is None else codigo
                print(f"Asiento {numero}: {estado}")
        elif opcion == "0":
            return
        else:
            print("Opción no válida")


def menu_espera(sistema):
    while True:
        print("\nLISTA DE ESPERA")
        print("1. Ver lista por vuelo")
        print("2. Retirar pasajero")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            id_vuelo = leer_entero("ID vuelo: ")
            if sistema.buscar_vuelo(id_vuelo) is None:
                print("El vuelo no existe.")
                continue
            cola = sistema.lista_espera.get(id_vuelo)
            if cola is None or cola.esta_vacia():
                print("Sin pasajeros en espera")
                continue
            copia = cola.copiar()
            puesto = 1
            while not copia.esta_vacia():
                cedula = copia.desencolar()
                print(f"{puesto}. {sistema.buscar_pasajero(cedula)}")
                puesto += 1
        elif opcion == "2":
            id_vuelo = leer_entero("ID vuelo: ")
            cedula = leer_texto("Cédula: ")
            ejecutar(sistema.retirar_espera, id_vuelo, cedula)
        elif opcion == "0":
            return
        else:
            print("Opción no válida")


def menu_itinerario(sistema):
    while True:
        print("\nITINERARIO")
        print("1. Ver itinerario")
        print("2. Agregar escala")
        print("3. Eliminar escala")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            return
        if opcion not in ("1", "2", "3"):
            print("Opción no válida")
            continue
        id_vuelo = leer_entero("ID vuelo: ")
        vuelo = sistema.buscar_vuelo(id_vuelo)
        if vuelo is None:
            print("El vuelo no existe.")
            continue
        ciudades = vuelo.itinerario.a_lista()
        for posicion, ciudad in enumerate(ciudades):
            print(f"{posicion}. {ciudad}")
        if opcion == "2":
            posicion = leer_entero("Posición de la nueva escala: ")
            ciudad = leer_texto("Ciudad: ")
            ejecutar(sistema.agregar_escala, id_vuelo, posicion, ciudad)
        elif opcion == "3":
            posicion = leer_entero("Posición de la escala: ")
            ejecutar(sistema.eliminar_escala, id_vuelo, posicion)


def menu():
    try:
        sistema = SistemaAerolinea()
    except (OSError, ValueError) as error:
        print(f"No se pudo iniciar: {error}")
        return
    print(f"Sistema iniciado: {len(sistema.pasajeros)} pasajeros, "
          f"{len(sistema.vuelos)} vuelos, {len(sistema.reservas)} reservas")
    while True:
        print("\nSISTEMA AEROLÍNEA")
        print("1. Agregar pasajero")
        print("2. Agregar vuelo")
        print("3. Reservar")
        print("4. Buscar vuelo por ID")
        print("5. Ruta entre ciudades")
        print("6. Ver reservas")
        print("7. Deshacer última acción")
        print("8. Salir")
        print("9. Gestionar pasajeros")
        print("10. Gestionar vuelos")
        print("11. Cancelar reserva")
        print("12. Lista de espera")
        print("13. Itinerario y escalas")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            agregar_pasajero(sistema)
        elif opcion == "2":
            agregar_vuelo(sistema)
        elif opcion == "3":
            reservar(sistema)
        elif opcion == "4":
            buscar_vuelo(sistema)
        elif opcion == "5":
            origen = leer_texto("Origen: ").title()
            destino = leer_texto("Destino: ").title()
            camino = sistema.red.camino_mas_corto(origen, destino)
            if camino is None:
                print("No hay ruta")
            else:
                print(" -> ".join(camino))
                print(f"Escalas: {max(0, len(camino) - 2)}")
        elif opcion == "6":
            mostrar_reservas(sistema)
        elif opcion == "7":
            ejecutar(sistema.deshacer)
        elif opcion == "8":
            try:
                sistema.guardar()
                print("Guardado. Adiós.")
                return
            except OSError:
                print("No se pudo guardar. Revise el archivo de datos.")
        elif opcion == "9":
            menu_pasajeros(sistema)
        elif opcion == "10":
            menu_vuelos(sistema)
        elif opcion == "11":
            codigo = leer_texto("Código de reserva: ").upper()
            ejecutar(sistema.cancelar_reserva, codigo)
        elif opcion == "12":
            menu_espera(sistema)
        elif opcion == "13":
            menu_itinerario(sistema)
        else:
            print("Opción no válida")
