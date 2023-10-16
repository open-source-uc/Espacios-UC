"""Miscellaneous: funciones varias del programa."""

import json
import time
from bs4 import BeautifulSoup
from threading import Thread
from os.path import isfile
from .open_parametros import parametros


def imprimir_cargando(hilo_padre: Thread, msg_final: str = "") -> None:
    """Función para un thread que se ejecuta en paralelo al thread principal, y
     y mostrara actividad en la consola si este sigue vivo."""
    while hilo_padre.is_alive():
        string = "Cargando"
        for i in range(4):
            if not hilo_padre.is_alive(): break
            print(f"{string}", end = "\r")
            time.sleep(0.5)
            string += "."
        print("\r\033[2K", end = "\r")
    print(msg_final)


def iniciales_campus(campus: str) -> str:
    """Obtiene las iniciales del campus para simplicar la identificación."""
    nombre_sep = campus.split()
    if len(nombre_sep) == 2: iniciales = (campus.split()[0][0], campus.split()[1][0])
    elif len(nombre_sep) == 1: iniciales = ("C", campus[0])
    return iniciales[0] + iniciales[1]


def convertir_a_json(diccionario: dict) -> str:
    """Convierte los diccionarios a json cambiando el set de la key
    por una tupla."""
    compatible = dict()
    for item in diccionario.items():
        if type(item[1]) == set: compatible[item[0]] = tuple(item[1])
        else: compatible[item[0]] = item[1]
    return json.dumps(compatible, ensure_ascii = False)


def revertir_a_dict(json_dict: str) -> dict:
    """Revierte el json a diccionario y devuelve la key a un set"""
    diccionario = json.loads(json_dict)
    reverto = dict()
    for item in diccionario.items():
        if type(item[1]) == list: reverto[item[0]] = set(item[1])
        else: reverto[item[0]] = item[1]
    return reverto


def abrir_leer_archivo(nombre_archivo: str, Bsplit: bool = True, spliter: str = ",", 
                       encoding1: str = None) -> list:
    '''Recibe el nombre de un archivo .txt y guarda cada linea en una lista, 
     y si se mantiene el parametro Bsplit en True tambien convierte cada linea 
     en una lista separada por el string splitter.'''
    archivo_abierto = open(nombre_archivo, 'r', encoding = encoding1)
    archivo_leido = archivo_abierto.readlines()
    archivo_abierto.close() 
    for linea in range(len(archivo_leido)):
        lista_de_linea = (archivo_leido[linea].strip("\n"))
        if Bsplit:
            lista_de_linea = lista_de_linea.split(spliter)
        archivo_leido[linea] = lista_de_linea
    return archivo_leido


def find_sp(number: int) -> str:
    """Encuentra el starting point de la iteración para el numero dado."""
    number = number - 1
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if number < 0: raise ValueError("El numero de busqueda debe ser natural")
    try: 
        f_letter_i = (number // 26)
        s_letter_i = number % 26
        return LETTERS[f_letter_i] + LETTERS[s_letter_i]
    except IndexError:
        raise IndexError("El numero de busqueda es mayor al" 
                         + " correspondiente al ultimo starting point.")


def log(data: str) -> None:
    """Registra información en el archivo de logs."""
    # if not isfile(parametros["name_logs"]): return None
    with open(parametros["name_logs"], "a", encoding = "utf-8") as archivo_parametros:
        print(f"[{time.ctime()}] -> {data}", 
              file = archivo_parametros)
        # print(f"[{(time.ctime(time.time())).split()[-2]}] -> {data}", 
        #       file = archivo_parametros)


def filtrar_modulo(modulo: str) -> bool:
    """Revisa si el modulo obtenido del collect es interpretable."""
    if (len(modulo) != 2) or not (modulo[1].isdigit()): return False 
    return (modulo[0] in parametros["dias"]) and (int(modulo[1]) in range(1, 10))
    

def verificar_modulo(modulo: str) -> None:
    """Levanta un error si el modulo entregado no es interpretable."""
    if not filtrar_modulo(modulo):
        raise ValueError("El horario elegido no existe. (Ej. formato: W5, L2, M3, S1)")


def verificar_campus(campus: str) -> None:
    """Levanta un error si el campus entregado no es interpretable."""
    if campus not in parametros["campus"]: 
        raise ValueError("El campus elegido no esta registrado en el programa."
                        + f" (Campus disponibles: {parametros['campus']})")
    
