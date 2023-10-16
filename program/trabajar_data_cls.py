"""Contiene la clase y las funciones con las que se almacenan y gestionan los datos."""

import time
from collections import defaultdict
from os.path import isfile
from .open_parametros import parametros
from .misc import (abrir_leer_archivo, revertir_a_dict, convertir_a_json, 
    iniciales_campus, filtrar_modulo, log, verificar_campus, verificar_modulo)


class ReadingError(Exception):
    """Información no leida correctamente"""
    def __init__(self) -> None:
        super().__init__(f"No se encontro el archivo {parametros['name_archivo']}\n" 
            + "Si estás actualizando los datos y aún no creas un nuevo archivo, puedes ignorar"
            + " este error. En caso contrario, puede ser un error en el directorio de ejecución.")


class DataManager():
    """Clase que almacena y gestiona los datos."""
    def __init__(self, new: bool = False) -> None:
        self.horarios = []
        self.salas = None
        if new: self.crear_dicts()
        elif isfile(parametros["name_archivo"]): 
            self.leer_informacion()
            #DEBUG log(f"DataManager creado con los archivos de {parametros['name_archivo']}")
        else: raise ReadingError()


    def reescribir_archivo(self, info: tuple) -> None:
        """Borra y sobreescribe la informacion del archivo por info."""
        archivo_abierto = open(parametros["name_archivo"], "w", encoding = "utf-8")
        for piece in info: print(piece, file = archivo_abierto)
        print(f"Ultima modificación: [{(time.ctime())}]", file = archivo_abierto)
        archivo_abierto.close()
        log(f"Datos guardados en {parametros['name_archivo']}")


    def crear_dicts(self) -> None:
        """Crea el archivo-plantilla para los datos.\n
        CORRERLA VA A BORRAR LOS DATOS EXISTENTES."""
        
        self.salas = defaultdict(set)

        str_safety = (f"Estas a punto de sobreescribir el archivo {parametros['name_archivo']}" 
            + " con una plantilla vacia, escribe SEGURO para continuar: ")
        safety = input(str_safety)
        if safety != "SEGURO": return None

        modulos = [(dia, bloque) for dia in parametros["dias"] for bloque in range(1, 10)]

        for c in parametros["campus"]:

            horario_campus = defaultdict(set)
            horario_campus["CAMPUS"] = iniciales_campus(c)

            for m in modulos:
                modulo = str(m[0]) + str(m[-1])
                horario_campus[modulo]

            self.horarios.append(horario_campus)

            self.salas[iniciales_campus(c)]

        self.guardar_datos()


    def leer_informacion(self) -> None:
        """Abre el archivo con los datos y guarda los diccionarios
          en los atributos de la instancia."""
        arch = abrir_leer_archivo(parametros["name_archivo"], 
                                  Bsplit = False, encoding1 = "utf-8")[:-1]
        self.salas = revertir_a_dict(arch.pop(0))
        for diccionario in arch: self.horarios.append(revertir_a_dict(diccionario))
        

    def añadir_datos(self, campus: str, dato: tuple) -> None:
        """Añade los datos entregados a los atributos de la instancia."""        
        # verificar_campus(campus)
        n = self.identificar_diccionario(campus)
        for m in dato[0]: 
            if not filtrar_modulo(m):
                log(f"NO SE PUDO INTERPRETAR -> modulo: {m} | sala: {dato[1]}")
                continue
            self.horarios[n][m].add(dato[1])
        self.salas[iniciales_campus(campus)].add(dato[1])


    def guardar_datos(self) -> None:
        """Escribe los datos almacenados por la instancia en un archivo."""
        info = []
        info.append(convertir_a_json(self.salas))
        for horario in self.horarios: info.append(convertir_a_json(horario))
        self.reescribir_archivo(info)


    def identificar_diccionario(self, campus: str) -> int:
        """Identifica el diccionario correspondiente a un campus."""
        # verificar_campus(campus)
        for i in range(len(self.horarios)):
            if self.horarios[i]["CAMPUS"] == iniciales_campus(campus): return i


    def salas_modulo(self, modulo: str, campus: str) -> set:
        """Retorna las salas ocupadas en el modulo dado."""
        # verificar_campus(campus)
        # verificar_modulo(modulo)
        n_diccionario = self.identificar_diccionario(campus)
        return set(self.horarios[n_diccionario].get(modulo))


    def encontrar_salas_vacias(self, modulo: str, campus: str) -> set:
        """Retorna las salas vacias en el modulo dado."""
        # verificar_campus(campus)
        # verificar_modulo(modulo)
        return set(filter(lambda x : x not in self.salas_modulo(modulo, campus),
                        self.salas[iniciales_campus(campus)]))
    

    def verificar_sala(self, sala: str, modulo: str, campus: str) -> bool:
        """Verifica si una sala esta vacia en el modulo dado."""
        # verificar_campus(campus)
        # verificar_modulo(modulo)
        if sala not in self.salas[iniciales_campus(campus)]: 
            raise ValueError("La sala ingresada no esta registrada en el programa")
        return sala in self.encontrar_salas_vacias(modulo, campus)

