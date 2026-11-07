from pasajero import Pasajero
from mi_pila import MiPila
from mi_cola import MiCola

pila = MiPila(10)
cola = MiCola(10)


# Funciones de apoyo.
def leer_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= 0:
                return numero
            print("El número no puede ser negativo.")
        except ValueError:
            print("Debe ser un número entero.")


def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Ingrese un dato.")


def leer_pasajero():
    nombre = leer_texto("Nombre: ")
    cedula = leer_texto("Cédula: ")
    edad = leer_entero("Edad: ")
    return Pasajero(nombre, cedula, edad)


def datos_prueba():
    return [
        Pasajero("Diana", "0923456789", 22),
        Pasajero("Ana", "0912345678", 28),
        Pasajero("Luis", "0987654321", 35),
        Pasajero("Beto", "0934567890", 16),
        Pasajero("Elena", "0901234567", 41),
    ]


def mostrar_opciones(titulo, entrar, salir, ver):
    print(f"\n{titulo}")
    print(f"1. {entrar}")
    print("2. Listar")
    print(f"3. {salir}")
    print(f"4. {ver}")
    print("5. Buscar por cédula")
    print("6. Modificar")
    print("7. Eliminar por cédula")
    print("8. Copiar")
    print("9. Longitud / ¿vacía?")
    print("10. Filtrar mayores de edad")
    print("11. Nombres en mayúsculas")
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
        elif op == "4":
            pasajero = pila.ver_tope()
            if pasajero is None:
                print("Pila vacía")
            else:
                print("Tope:", pasajero)
        elif op == "5":
            cedula = leer_texto("Cédula: ")
            pos = pila.buscar(cedula)
            if pos == -1:
                print("No existe")
            else:
                print(f"Encontrado en [{pos}]: {pila.datos[pos]}")
        elif op == "6":
            cedula = leer_texto("Cédula: ")
            nombre = leer_texto("Nuevo nombre: ")
            edad = leer_entero("Nueva edad: ")
            if pila.modificar(cedula, nombre, edad):
                print("Pasajero modificado")
        elif op == "7":
            cedula = leer_texto("Cédula: ")
            if pila.eliminar_por_cedula(cedula):
                print("Pasajero eliminado")
        elif op == "8":
            copia = pila.copiar()
            print("Copia de la pila")
            copia.listar()
        elif op == "9":
            print("Longitud:", pila.longitud())
            print("Está vacía:", pila.esta_vacia())
        elif op == "10":
            mayores = pila.filtrar_mayores_de_edad()
            print("Mayores de edad")
            mayores.listar()
        elif op == "11":
            nombres = pila.nombres_en_mayusculas()
            print("Nombres en mayúsculas:", nombres)
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
        elif op == "4":
            pasajero = cola.ver_frente()
            if pasajero is None:
                print("Cola vacía")
            else:
                print("Frente:", pasajero)
        elif op == "5":
            cedula = leer_texto("Cédula: ")
            pos = cola.buscar(cedula)
            if pos == -1:
                print("No existe")
            else:
                print(f"Encontrado en [{pos}]: {cola.datos[pos]}")
        elif op == "6":
            cedula = leer_texto("Cédula: ")
            nombre = leer_texto("Nuevo nombre: ")
            edad = leer_entero("Nueva edad: ")
            if cola.modificar(cedula, nombre, edad):
                print("Pasajero modificado")
        elif op == "7":
            cedula = leer_texto("Cédula: ")
            if cola.eliminar_por_cedula(cedula):
                print("Pasajero eliminado")
        elif op == "8":
            copia = cola.copiar()
            print("Copia de la cola")
            copia.listar()
        elif op == "9":
            print("Longitud:", cola.longitud())
            print("Está vacía:", cola.esta_vacia())
        elif op == "10":
            mayores = cola.filtrar_mayores_de_edad()
            print("Mayores de edad")
            mayores.listar()
        elif op == "11":
            nombres = cola.nombres_en_mayusculas()
            print("Nombres en mayúsculas:", nombres)
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
