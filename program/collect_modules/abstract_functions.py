"""Funciones para la realización y lectura del request."""

import requests
from bs4 import BeautifulSoup
from program.open_parametros import parametros
from program.misc import verificar_campus, verificar_modulo

#G Si te estas preguntando porque no estan en misc, yo tambien
#G pero mi yo del pasado lo decidio así y no voy a cuestionar las
#G decisiones de ese loco.

def realizar_get_abst(modulo: str|None = None, campus: str = "San Joaquín", sigla: str = "") -> BeautifulSoup:
    """Realiza el get a buscacursos y lo convierte al formato BS"""
    if (modulo != None): verificar_modulo(modulo)
    verificar_campus(campus)
    campus = campus.replace(" ", "+")
    if modulo: last_cxml = f"&cxml_modulo_{modulo}={modulo}"
    else: last_cxml = ""
    url = f"https://buscacursos.uc.cl/?cxml_semestre={parametros['year']}-{parametros['semestre']}&cxml_sigla={sigla}&cxml_campus={campus}{last_cxml}#resultados"
    # "https://ramosuc.cl/p_search?overlap=false&page=1&campus%5B%5D=San%20Joaqu%C3%ADn&credits=&free_quota=false&max_mod=&overlap_except=false&period=2023-2&q=&schedule=&without_req=false"
    html_data = requests.get(url)
    return BeautifulSoup(html_data.text, "html.parser")

def clear_data_abst(data: BeautifulSoup) -> list:
    """Extrae exclusivamente los datos de los ramos"""
    ramos = list(data.find_all('tr', class_ = "resultadosRowImpar")) + list(data.find_all('tr', class_ = "resultadosRowPar"))
    return ramos


def separar_dias(string: str) -> tuple: 
    '''Funcion para adaptar el formato de los modulos al formato D0.'''
    horarios = []
    string = string.split(":")
    dias = string[0].split("-")
    modulos = string[-1].split(",")
    for dia in dias:
        for modulo in modulos:
            horario = dia + modulo
            horarios.append(horario)
    return tuple(horarios)


def despejar_cuadro_hora(sopa_html: BeautifulSoup) -> list:
    '''Esta funcion despeja el cuadro donde se encuentra las horas y salas
    del ramo y los ordena. \n
    Retorna una lista con tuplas ((modulos), sala).'''
    horarios = []
    lista_del_cuadro = (sopa_html.find("td", style = "text-align:left;")).text 
    lista_del_cuadro = (lista_del_cuadro).strip("\n").split("\n\n\n\n\n")
    for horario in lista_del_cuadro:
        horario = horario.split("\n\n\n")
        if horario[0] in {":", ""}: continue
        elif len(horario) != 3:
            print(f"Estos datos tiene un formato que no se pudo interpretar {horario}")
            continue 
        dias = horario[0]
        horario[0] = separar_dias(dias)
        horario.pop(1)
        horarios.append(tuple(horario))
    return horarios



