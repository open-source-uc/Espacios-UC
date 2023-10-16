"""Mini programa para realizar más comodamente las busquedas en el BuscaCursos."""

from program.trabajar_data_cls import DataManager, ReadingError, verificar_campus
from program.collect_modules.collect_data import BuscarDatosThread
from threading import Thread
import sys

#* ESTE ARCHIVO SE MODIFICA MANUALMENTE PARA BUSCAR DE A POCO LA INFORMACIÓN
#G Para ejecutar se deben modificar y descomentar cosas segun se necesite


CREAR_ARCH = False
CAMPUS = "San Joaquín"
N_BUSQUEDA = 1 #! Ese el numero de la ULTIMA busqueda
N_MAX = 4
#G Se deben realizar 676 busquedas

verificar_campus(CAMPUS)

def buscar(n_busqueda: int):
    """Realiza una busqueda en el buscacursos"""
    buscador = BuscarDatosThread(CAMPUS, n_busqueda)
    buscador.start()
    while buscador.is_alive(): pass
    for tupla in buscador.tuplas_horarios: Gestor.añadir_datos(CAMPUS, tupla)
    Gestor.guardar_datos()


def automatico(I: int, F: int):
    for n in range(I, F + 1): buscar(n)


if __name__ == '__main__':

    if CREAR_ARCH: DataManager(new = True)
    
    else:
        Gestor = DataManager()
        
        if len(sys.argv) > 1:
            N_BUSQUEDA = int(sys.argv[1])
            N_MAX = int(sys.argv[2])
            if len(sys.argv) > 3: CAMPUS = sys.argv[3]

        # buscar(N_BUSQUEDA)
        automatico(N_BUSQUEDA, N_MAX)
