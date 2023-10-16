"""Contiene el Thread y las funciones para recopilar los datos."""

import time
from threading import Thread
from .abstract_functions import realizar_get_abst, clear_data_abst, despejar_cuadro_hora
from ..open_parametros import parametros
from ..misc import imprimir_cargando, find_sp, log, verificar_campus


def iteracion_get(campus_i: str, sigla_i: str) -> list:
    """Realiza un get con los parametros especificados y retorna la información de los ramos"""
    return clear_data_abst(realizar_get_abst(campus = campus_i, sigla = sigla_i))


def collect(campus: str, search_number: int) -> list:
    """Realiza busquedas en BC, iterando la sigla de ramo a partir de 2 letras base. \n
    By Felipe Correa. \n
    Based on https://github.com/open-source-uc/ramos-uc/blob/main/apps/bc_scraper/actions/collect.py. \n
    Descripcion original: \"Iterates a search throw all BC and process all courses and sections found.\" \n"""    
    
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    NUMBERS = "0123456789"

    start_point = find_sp(search_number)

    tuplas_horarios = []

    try:
        t_inicio_proceso = time.time()
        for l3 in LETTERS:
            t_inicio = time.time()
            comb = start_point + l3
            courses = iteracion_get(campus, comb)
            if len(courses) < 50: 
                t_final = time.time()
                for curso in courses: 
                    for h in despejar_cuadro_hora(curso): tuplas_horarios.append(h)
                if 0 < len(courses): log(f"comb exitoso: {comb} - N°{search_number} - Tiempo:" 
                    + f" {str(t_final - t_inicio)[:6]} segundos - Se recibio la informacion de" 
                    + f" {len(courses)} ramos")
                continue
            for n1 in NUMBERS:
                comb = start_point + l3 + n1
                courses = iteracion_get(campus, comb)
                if len(courses) < 50: 
                    t_final = time.time()
                    for curso in courses: 
                        for h in despejar_cuadro_hora(curso): tuplas_horarios.append(h)
                    if 0 < len(courses): log(f"comb exitoso: {comb} - N°{search_number} - Tiempo:" 
                        + f" {str(t_final - t_inicio)[:6]} segundos - Se recibio la informacion de" 
                        + f" {len(courses)} ramos")
                    continue

                for n2 in NUMBERS:
                    comb = start_point + l3 + n1 + n2
                    courses = iteracion_get(campus, comb)
                    if len(courses) < 50: 
                        t_final = time.time()
                        for curso in courses: 
                            for h in despejar_cuadro_hora(curso): tuplas_horarios.append(h)
                        if 0 < len(courses): log(f"comb exitoso: {comb} - N°{search_number} - Tiempo:" 
                            + f" {str(t_final - t_inicio)[:6]} segundos - Se recibio la informacion de" 
                            + f" {len(courses)} ramos")
                        continue

                    #? New
                    for n3 in NUMBERS:
                        comb = start_point + l3 + n1 + n2 + n3
                        courses = iteracion_get(campus, comb)
                        t_final = time.time()
                        if 0 < len(courses): log(f"comb exitoso: {comb} - N°{search_number} - Tiempo:" 
                            + f" {str(t_final - t_inicio)[:6]} segundos - Se recibio la informacion de" 
                            + f" {len(courses)} ramos")
                        if len(courses) == 50: log(f"Maybe something went wrong with comb: {comb}") 
                        for curso in courses: 
                            for h in despejar_cuadro_hora(curso): tuplas_horarios.append(h)
        
        t_final_proceso = time.time()
        log(f"BUSQUEDA N°{search_number} / SP:{start_point} / CAMPUS: {campus} FINALIZADA - Tiempo total: " 
            + f"{str(t_final_proceso - t_inicio_proceso)[:6]} segundos")
        return tuplas_horarios

    except Exception as err:
        log(err + f"\n Ultimo comb: {comb}")
        raise err


class BuscarDatosThread(Thread):
    """Thread que realiza la iteración de los gets"""
    def __init__(self, campus: str, search_number: int) -> None:
        super().__init__()
        self.name = f"Buscador de datos {search_number}"
        self.sn = search_number
        self.start_point = find_sp(search_number)
        verificar_campus(campus)
        self.campus = campus
        self.tuplas_horarios = None

    def run(self):
        cargando = Thread(target = imprimir_cargando, args = [self, 
            f"BUSQUEDA {self.campus} - {self.start_point}: Terminada"], daemon = False)
        cargando.start()
        self.tuplas_horarios = collect(self.campus, self.sn)
