# BUSCADOR DE SALAS VACIAS

### Para buscar una sala 
* Se debe ejecutar el archivo `main.py` en el directorio donde se encuentra la carpeta `program`. (Sacar `main.py` de su carpeta o ejecutar desde VScode puede dar error)
* Seguir las instrucciones de la consola, el formato de los modulos es `D0`, Dia-Numero, por ejemplo el tercer modulo del jueves seria `J3`.

### Para actualizar la información 
* Se deben tener instalados los modulos `requests` y `bs4`. 
* Se debe encontrar en el directorio `program` la carpeta `collect_modules`. (Además del resto del programa).
    #### Ejecución de las busquedas
    1. Actualizar los parametros "`year`" y "`semestre`"en el archivo `parametros.json`.
    2. **Abrir** `main_collect.py` en el directorio donde se encuentra la carpeta `program`, este modulo no esta hecho para ejecutarse sin más, la idea es hacer las busquedas de a poco y de manera controlada, por lo que lo ideal es abrirlo e irlo modificando. Se debe cambiar el parametro `CREAR_ARCH` a True, esto solo debe hacerse la primera vez. Luego se deben realizar 676 busquedas, numeradas desde el 1 al 676, estas busquedas representan los prefijos con los que se buscan los ramos desde "AA" hasta "ZZ". `N_BUSQUEDA` y `N_MAX` se deben ir variando según sea necesario
    3. Los datos se guardaran en diccionarios en el archivo con el nombre de "`DATA_{año}-{semestre}.txt`".  Por otro lado el archivo de `extraction_logs_{año}-{semestre}.txt` registrara información que pueda resultar relevante sobre el avance de las busquedas.
    **En teoria** para añadir otro campus bastaria con añadirlo a los parametros y hacer sus busquedas.

### Para trabajar con el codigo
* Los prefijos en los comentarios son irrelevantes, estos pertecen a una personalizacion de una extension de VScode y no cumplen otro objetivo más que facilitarme la lectura. En cualquier caso sus significados son los siguientes:
    * `# `: Representan una linea tachada u oculta del codigo
    * `#? `: Representan una explicación o apunte sobre el codigo
    * `#G `: Representan un comentario general, no apuntan tanto a la comprension del codigo sino más bien a detalles sobre este o notas sobre el origen del codigo
    * `#* `: No representan nada, solo son más visibles que los demás comentarios, le dan cierta jerarquia a la información
    * `#! `: Representan información importante que se debe tener en cuenta antes de ejecutar el codigo
    * `#TODO `: Representan una idea o arreglo pendiente
    * `#Debug `: Representan una linea que se ocupa para debuggear el codigo


#### **Recomendación personal si estas en windows:**
* Crea un acceso directo a CMD en el escritorio
* En propiedades, añade al final del destino `/c python main.py`
* En la direccion de inicio escribe la dirección en que se encuentra el programa

