"""Menus y funciones relevantes a estos."""

import sys
from .open_parametros import parametros
from .trabajar_data_cls import DataManager
from .misc import verificar_modulo

#G Para los strings, se recomienda checkear:
#G https://gist.github.com/458719343aabd01cfb17a3a4f7296797.git

def titulo(campus: str = "", modulo: str = "") -> None:
    """Imprime el titulo del programa, adaptando si ya se selecciono campus o modulo."""
    sys.stdout.write("\033[H\033[J")
    titulo = "BUSCADOR DE SALAS"
    if campus: campus = f"CAMPUS: \033[34m\033[3m{campus}\033[0m\n\n"
    else: campus = ""
    if modulo: 
        modulo = f"MODULO: \033[34m{modulo}\033[0m\n\n"
        campus = campus[:-1]
    else: modulo = ""
    separador = "=" * 27
    print(f"\n\033[4m\033[1m{titulo}\033[0m\n\n{campus}{modulo}\033[38;5;237m" 
          + f"{separador}\033[39m\n")


def num_bonito(num: int) -> str:
    """Genera el string para las opciones."""
    return f"\033[38;5;237m[\033[39m{num}\033[38;5;237m]\033[39m"


def str_modulo(numero_modulo: int) -> str:
    """Retorna el string formateado para el modulo correspondiente."""
    if numero_modulo <= 4:
        return (f"{numero_modulo} -> {parametros['horas_m'][numero_modulo - 1]}" 
                + f" - {parametros['horas_m'][numero_modulo]}")
    elif numero_modulo > 4: 
        return (f"{numero_modulo} -> {parametros['horas_t'][numero_modulo - 5]}" 
                + f" - {parametros['horas_t'][numero_modulo - 4]}")


def menu_opciones(solicitud: str, opciones: list|tuple) -> int|None:
    """Despliega un menu generico para elegir entre opciones."""
    str_opt = f"{solicitud}:\n\n    {num_bonito(0)} Salir\n"
    for n_opt in range(len(opciones)): 
        str_opt += f"    {num_bonito(n_opt + 1)} \033[1m{opciones[n_opt]}\033[0m\n"
    print(str_opt)
    while True:
        opcion = input("Escriba numero de opcion: ")
        if opcion not in set(str(i) for i in range(len(opciones) + 1)): 
            print("\033[2K\033[F\n\033[F\033[91m\033[3mIngrese una opción valida\033[0K\033[0m")
        elif opcion == "0":
            print("\nSaliendo del programa...")
            sys.exit()
        else: return int(opcion)


def imprimir_cuadro(info: list|tuple, titulo: str|None = None,
            margen: int = 3, diff_titulo: int = 2) -> None:
    """Imprime el cuadro con la numeración de los modulos."""
    str_final = ""
    mx = 0
    for i in info: 
        if len(i) > mx: mx = len(i)
    for i in info:
        str_final += f"│{' ' * margen}{i.center(mx)}{' ' * margen}│\n"
    str_final += f"└{'─' * (mx + (margen * 2))}┘"
    if titulo: 
        str_final = (f"│{' ' * (margen - diff_titulo)}\033[1m{titulo}\033[0m"
                    + f"{' ' * (mx - len(titulo) + margen + diff_titulo)}│\n├"
                    + f"{'─' * (mx + (margen * 2))}┤\n" + str_final)
    str_final = f"┌{'─' * (mx + (margen * 2))}┐\n" + str_final
    print(str_final + "\n")


def menu_selec_campus() -> str:
    """Menu simple para elegir campus."""
    opt = menu_opciones("SELECCIONAR CAMPUS", parametros["campus"])
    return parametros["campus"][opt - 1]


def menu_selec_modulo() -> str:
    """Menu simple para elegir modulo."""
    imprimir_cuadro([str_modulo(x) for x in range(1, 10)], "Modulos:", diff_titulo = 2)
    while True:
        modulo = input("Modulo a buscar (0 para salir): ")
        if modulo == "0": 
            print("\nSaliendo del programa...")
            sys.exit()
        try: 
            verificar_modulo(modulo)
            return modulo
        except ValueError as err:
            print("\033[F\033[2K", err, sep = "")


def menu_inicial(campus: str|None = None, modulo: str|None = None) -> None:
    """Menu inicial del programa, donde se elige el campus y el modulo."""
    titulo(campus, modulo)
    if not campus: 
        titulo(campus, modulo)
        campus = menu_selec_campus()
    if not modulo: 
        titulo(campus, modulo)
        modulo = menu_selec_modulo()
    return menu_buscar(campus, modulo)


def menu_buscar(campus: str, modulo: str) -> None:
    """Menu del programa donde se elige y se ejecuta la accion a realizar, tambien es donde se 
    crea el DataManager."""
    manager = DataManager()
    titulo(campus, modulo)

    opt = menu_opciones("ACCIÓN", ("Buscar salas desocupadas", "Comprobar estado de sala",
                                    "Cambiar campus", "Cambiar modulo"))
    sys.stdout.write("\033[F\033[2K")

    if opt == 1: #? Buscar salas desocupadas
        vacias = list(manager.encontrar_salas_vacias(modulo, campus))
        vacias.sort()
        titulo(campus, modulo)
        print("Las siguientes salas estan desocupadas:\n")
        for n in range(len(vacias)):
            print(f"{str(n + 1).zfill(3)}-. {vacias[n]}")
        print()
    
    elif opt == 2: #? Comprobar estado sala
        while True: 
            sala = input("Sala a buscar (0 para salir): ")
            if sala == "0": 
                print("\nSaliendo del programa...")
                sys.exit()
            try: 
                vacia = manager.verificar_sala(sala, modulo, campus)
                break
            except ValueError as err:
                print("\033[F\033[2K", err, sep = "")
        titulo(campus, modulo)
        respuesta = f"La sala {sala} está "
        if vacia: respuesta += "\033[32mVACIA\033[39m\n"
        else: respuesta += "\033[31mOCUPADA\033[39m\n"
        print(respuesta)

    elif opt == 3: #? Cambiar campus
        return menu_inicial(modulo = modulo)
    
    elif opt == 4: #? Cambiar modulo
        return menu_inicial(campus = campus)
    
    opt = menu_opciones("ACCIÓN", ["Volver a buscar"])
    if opt == 1: return menu_buscar(campus, modulo)
