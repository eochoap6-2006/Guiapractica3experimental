from datetime import date

from pasajero import Pasajero
from mi_pila import MiPila
from mi_cola import MiCola

pila = MiPila(10)
cola = MiCola(10)


# Funciones de apoyo.
def leer_entero(mensaje, minimo=0):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo:
                return numero
            print(f"Ingrese un número desde {minimo}.")
        except ValueError:
            print("Debe ser un número entero.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Ingrese un dato.")


def leer_pasajero():
    numero = leer_entero("Número de pasajero: ", 1)
    nombre = leer_texto("Nombre: ")
    cedula = leer_texto("Cédula: ")
    edad = leer_entero("Edad: ")
    fecha = leer_fecha()
    destino = leer_texto("Destino: ")
    asiento = leer_texto("Asiento: ").upper()
    return Pasajero(numero, nombre, cedula, edad, fecha, destino, asiento)


def leer_fecha():
    while True:
        fecha = input("Fecha de vuelo (AAAA-MM-DD): ").strip()
        try:
            if date.fromisoformat(fecha).isoformat() == fecha:
                return fecha
        except ValueError:
            pass
        print("Ingrese una fecha válida con el formato AAAA-MM-DD.")


def datos_prueba():
    return [
        Pasajero(1005, "Diana", "0923456789", 22, "2026-11-15", "Quito", "12A"),
        Pasajero(1002, "Ana", "0912345678", 28, "2026-11-15", "Lima", "03C"),
        Pasajero(1009, "Luis", "0987654321", 35, "2026-11-20", "Bogotá", "18F"),
        Pasajero(1004, "Beto", "0934567890", 16, "2026-11-20", "Quito", "07B"),
        Pasajero(1001, "Elena", "0901234567", 41, "2026-11-22", "Lima", "01A"),
    ]


def mostrar_opciones(titulo, entrar, salir, ver):
    print(f"\n{titulo}")
    print(f"1. {entrar}")
    print("2. Listar")
    print(f"3. {salir}")
    print(f"4. {ver}")
    print("5. Buscar por número")
    print("6. Modificar destino y asiento")
    print("7. Eliminar por número")
    print("8. Copiar")
    print("9. Longitud / ¿vacía?")
    print("C. Cargar datos de prueba")
    print("0. Volver")


# Menú de pila.
def menu_pila():
    while True:
        mostrar_opciones("MENÚ 1 - PILA (LIFO)", "Apilar", "Desapilar", "Ver tope")
        op = input("Opción: ").strip().upper()

        if op == "1":
            pasajero = leer_pasajero()
            if pila.apilar(pasajero):
                print("Pasajero apilado")
        elif op == "2":
            pila.listar()
        elif op == "3":
            pasajero = pila.desapilar()
            if pasajero is None:
                print("Pila vacía")
            else:
                print("Salió:", pasajero)
                nuevo = pila.ver_tope()
                if nuevo is None:
                    print("Pila vacía")
                else:
                    print("Nuevo tope:", nuevo)
        elif op == "4":
            pasajero = pila.ver_tope()
            if pasajero is None:
                print("Pila vacía")
            else:
                print("Tope:", pasajero)
        elif op == "5":
            numero = leer_entero("Número de pasajero: ", 1)
            pos = pila.buscar(numero)
            if pos == -1:
                print("No existe")
            else:
                print(f"Encontrado en [{pos}]: {pila.datos[pos]}")
        elif op == "6":
            numero = leer_entero("Número de pasajero: ", 1)
            destino = leer_texto("Nuevo destino: ")
            asiento = leer_texto("Nuevo asiento: ").upper()
            if pila.modificar(numero, destino, asiento):
                print("Pasajero modificado")
        elif op == "7":
            numero = leer_entero("Número de pasajero: ", 1)
            if pila.eliminar_por_numero(numero):
                print("Pasajero eliminado")
        elif op == "8":
            copia = pila.copiar()
            print("Copia de la pila")
            copia.listar()
        elif op == "9":
            print("Longitud:", pila.longitud())
            print("Está vacía:", pila.esta_vacia())
        elif op == "C":
            for pasajero in datos_prueba():
                pila.apilar(pasajero)
            print("Datos de prueba cargados")
        elif op == "0":
            break
        else:
            print("Opción no válida")


# Menú de cola.
def menu_cola():
    while True:
        mostrar_opciones("MENÚ 2 - COLA (FIFO)", "Encolar", "Desencolar", "Ver frente")
        op = input("Opción: ").strip().upper()

        if op == "1":
            pasajero = leer_pasajero()
            if cola.encolar(pasajero):
                print("Pasajero encolado")
        elif op == "2":
            cola.listar()
        elif op == "3":
            pasajero = cola.desencolar()
            if pasajero is None:
                print("Cola vacía")
            else:
                print("Salió:", pasajero)
                nuevo = cola.ver_frente()
                if nuevo is None:
                    print("Cola vacía")
                else:
                    print("Nuevo frente:", nuevo)
        elif op == "4":
            pasajero = cola.ver_frente()
            if pasajero is None:
                print("Cola vacía")
            else:
                print("Frente:", pasajero)
        elif op == "5":
            numero = leer_entero("Número de pasajero: ", 1)
            pos = cola.buscar(numero)
            if pos == -1:
                print("No existe")
            else:
                print(f"Encontrado en [{pos}]: {cola.datos[pos]}")
        elif op == "6":
            numero = leer_entero("Número de pasajero: ", 1)
            destino = leer_texto("Nuevo destino: ")
            asiento = leer_texto("Nuevo asiento: ").upper()
            if cola.modificar(numero, destino, asiento):
                print("Pasajero modificado")
        elif op == "7":
            numero = leer_entero("Número de pasajero: ", 1)
            if cola.eliminar_por_numero(numero):
                print("Pasajero eliminado")
        elif op == "8":
            copia = cola.copiar()
            print("Copia de la cola")
            copia.listar()
        elif op == "9":
            print("Longitud:", cola.longitud())
            print("Está vacía:", cola.esta_vacia())
        elif op == "C":
            for pasajero in datos_prueba():
                cola.encolar(pasajero)
            print("Datos de prueba cargados")
        elif op == "0":
            break
        else:
            print("Opción no válida")


# Menú principal.
def main():
    while True:
        print("\nTAREA PILAS Y COLAS - PASAJEROS")
        print("1. Menú 1 - Pila")
        print("2. Menú 2 - Cola")
        print("3. Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_pila()
        elif op == "2":
            menu_cola()
        elif op == "3":
            print("Hasta pronto")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
