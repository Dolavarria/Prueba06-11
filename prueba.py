from datetime import datetime

def leer_reservas(nombre_archivo: str) -> dict:
    reservas = {}
    try:
        with open(nombre_archivo, 'r') as file:
            for line in file:
                datos = line.strip().split(',')
                id_reserva = datos[0]
                reservas[id_reserva] = {
                    'nombre_usuario': datos[1],
                    'tipo_sala': datos[2],
                    'fecha_reserva': datos[3],
                    'hora_inicio': datos[4],
                    'hora_fin': datos[5],
                    'costo_reserva': float(datos[6])
                }
    except FileNotFoundError:
        print("El archivo no se encontró.")
    else:
        print("Archivo leído correctamente.")
    return reservas

def usuarios_en_fecha(reservas: dict, tipo_sala: str, fecha_consulta: str):
    usuarios = [
        reserva['nombre_usuario']
        for reserva in reservas.values()
        if reserva['tipo_sala'].lower() == tipo_sala.lower() and reserva['fecha_reserva'] == fecha_consulta
    ]
    print(f"Usuarios que reservaron {tipo_sala} en {fecha_consulta}:")
    if usuarios:
        for usuario in usuarios:
            print(usuario)
    else:
        print("No se encontraron reservas para los criterios especificados.")


def cantidad_reservas_usuario(reservas: dict, usuario: str, f_inicio: str, f_fin: str):
    from datetime import datetime
    inicio = datetime.strptime(f_inicio, '%Y-%m-%d')
    fin = datetime.strptime(f_fin, '%Y-%m-%d')
    count = sum(1 for reserva in reservas.values()
                if reserva['nombre_usuario'] == usuario and inicio <= datetime.strptime(reserva['fecha_reserva'], '%Y-%m-%d') <= fin)
    print(f"Cantidad total de reservas de {usuario} entre {f_inicio} y {f_fin}: {count}")

def usuarios_en_horario(reservas: dict, h_inicio: str, h_fin: str):
    # Convert string times to datetime objects for comparison
    formato = '%H:%M'
    inicio_consulta = datetime.strptime(h_inicio, formato)
    fin_consulta = datetime.strptime(h_fin, formato)
    
    usuarios = []
    for reserva in reservas.values():
        reserva_inicio = datetime.strptime(reserva['hora_inicio'], formato)
        reserva_fin = datetime.strptime(reserva['hora_fin'], formato)
        
        # Verificar si hay superposición en los horarios
        if reserva_inicio < fin_consulta and reserva_fin > inicio_consulta:
            usuarios.append(reserva['nombre_usuario'])
    
    print(f"Usuarios que usaron una sala de estudios entre {h_inicio} y {h_fin}:")
    if usuarios:
        for usuario in usuarios:
            print(usuario)
    else:
        print("No se encontraron usuarios en el horario especificado.")


def usuario_frecuente_sala(reservas: dict, usuario: str, tipo_sala: str, cant_minima: int):
    count = sum(1 for reserva in reservas.values()
                if reserva['nombre_usuario'] == usuario and reserva['tipo_sala'] == tipo_sala)
    if count > cant_minima:
        print(f"{usuario} reservó {tipo_sala} más de {cant_minima} veces.")
    else:
        print(f"{usuario} no reservó {tipo_sala} más de {cant_minima} veces.")

def iniciar_analisis():
    reservas = leer_reservas('reservas_salas.txt')
    if not reservas:
        print("No hay reservas para analizar.")
        return    
    usuarios_en_fecha(reservas, 'Sala individual', '2024-11-15')
    cantidad_reservas_usuario(reservas, 'Juan Perez', '2024-11-01', '2024-11-18')
    usuarios_en_horario(reservas, '09:00', '11:00')
    usuario_frecuente_sala(reservas, 'Maria Gomez', 'Sala individual', 1)

iniciar_analisis()