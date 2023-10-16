"""Abre el archivo JSON con los parametros globales."""

import os
import json

dire = os.path.dirname(os.path.abspath(__file__)) 
#G From StackOverflow https://stackoverflow.com/questions/4187300/

with open(os.path.join(dire, "parametros.json"), encoding = "utf-8") as archivo_parametros:
    parametros_json = archivo_parametros.read()
    parametros: dict = json.loads(parametros_json)

#? Los nombres de archivo se crean acá para no tener que modificarlos con la fecha
parametros["name_archivo"] = f"program/DATA_{parametros['year']}-{parametros['semestre']}.txt" 
parametros["name_logs"] = (
    f"program/collect_modules/extraction_log_{parametros['year']}-{parametros['semestre']}.txt"
    )

# "name_archivo": "program/DATA_2023-2.txt", 
# "name_logs": "program/collect_modules/extraction_log_2023-2.txt"



