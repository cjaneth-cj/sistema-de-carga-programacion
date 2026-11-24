import modulo_json

datos_activos = []
datos_eliminados = []
ids_registrados = set()

def inicializar_sistema():
    """Carga los datos y sincroniza el conjunto de claves primarias."""
    global datos_activos, datos_eliminados, ids_registrados
    datos_activos, datos_eliminados = modulo_json.cargar_json()

    ids_registrados = set()
    # Use .strip().lower() para comparar sin importar espacios o mayúsculas
    for serie in datos_activos:
        ids_registrados.add(str(serie["codigo"]).strip().lower())
    for serie in datos_eliminados:
        ids_registrados.add(str(serie["codigo"]).strip().lower())

def existe_codigo(codigo):
    """Verifica si el código ingresado ya fue registrado."""
    return str(codigo).strip().lower() in ids_registrados

def agregar_kdrama(codigo, titulo, genero, plataforma, episodios):
    """Agrega una nueva serie aplicando .strip(), .upper() y .title()."""
    codigo_norm = str(codigo).strip()

    if existe_codigo(codigo_norm):
        return (
            False,
            f"El código '{codigo_norm.upper()}' ya se encuentra registrado.",
        )

    #
    nuevo_kdrama = {
        "codigo": codigo_norm.upper(),
        "titulo": titulo.strip().title(),
        "genero": genero.strip().title(),
        "plataforma": plataforma.strip(),
        "episodios": int(episodios),
    }

    datos_activos.append(nuevo_kdrama)
    ids_registrados.add(codigo_norm.lower())
    modulo_json.guardar_json(datos_activos, datos_eliminados)
    return True, f"K-Drama '{nuevo_kdrama['titulo']}' agregado exitosamente."

def buscar_kdrama_activo(busqueda):
    """Busca por código o por título usando .lower() para evitar errores por mayúsculas/minúsculas."""
    termino = str(busqueda).strip().lower()

    for serie in datos_activos:
        codigo_actual = str(serie["codigo"]).strip().lower()
        titulo_actual = str(serie["titulo"]).strip().lower()

        if termino == codigo_actual or termino in titulo_actual:
            return serie
    return None

def baja_logica(codigo):
    """Traslada una serie de la lista de disponibles a la lista de retirados."""
    codigo_norm = str(codigo).strip().lower()

    for serie in datos_activos:
        if str(serie["codigo"]).strip().lower() == codigo_norm:
            datos_activos.remove(serie)
            datos_eliminados.append(serie)
            modulo_json.guardar_json(datos_activos, datos_eliminados)
            return (
                True,
                f"Baja lógica realizada: '{serie['titulo']}' fue retirada de la plataforma.",
            )

    return False, "La serie no se encuentra activa o disponible."

def reactivar_kdrama(codigo):
    """Reactiva una serie que fue dada de baja (vuelve a estar disponible)."""
    codigo_norm = str(codigo).strip().lower()

    for serie in datos_eliminados:
        if str(serie["codigo"]).strip().lower() == codigo_norm:
            datos_eliminados.remove(serie)
            datos_activos.append(serie)
            modulo_json.guardar_json(datos_activos, datos_eliminados)
            return (
                True,
                f"Reactivación exitosa: '{serie['titulo']}' vuelve a estar disponible.",
            )

    return False, "La serie no se encuentra en la lista de eliminados."