import sqlite3

def conectar():
    conexion = sqlite3.connect("tutorias.db")
    return conexion

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL, -- 'estudiante' o 'tutor'
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            edad INTEGER, -- para ambos
            materia TEXT, -- solo estudiantes
            especialidad TEXT -- solo para tutores
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tutorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER,
            tutor_id INTEGER,
            fecha TEXT,
            hora TEXT,
            materia TEXT,
            estado TEXT,
            FOREIGN KEY (estudiante_id) REFERENCES usuarios(id),
            FOREIGN KEY (tutor_id) REFERENCES usuarios(id)
        )
    """)

    conexion.commit()
    conexion.close()

class Usuario:
    def __init__(self, nombre, apellido, correo, contrasena, edad):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.edad = edad

class Estudiante(Usuario):
    def __init__(self, nombre, apellido, correo, contrasena,edad, materia):
        super().__init__(nombre, apellido, correo, contrasena, edad)
        self.materia = materia

class Tutor(Usuario):
    def __init__(self, nombre, apellido, correo, contrasena, edad, especialidad):
        super().__init__(nombre, apellido, correo, contrasena, edad)
        self.especialidad = especialidad

def registrar_usuario(usuario, tipo):
    conexion = conectar()
    cursor = conexion.cursor()

    if tipo == "estudiante":
        cursor.execute("INSERT INTO usuarios (tipo, nombre, apellido, correo, contrasena, edad, materia) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (tipo, usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena, usuario.edad,usuario.materia))
    elif tipo == "tutor":
        cursor.execute("INSERT INTO usuarios (tipo, nombre, apellido, correo, contrasena, edad, especialidad) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (tipo, usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena, usuario.edad, usuario.especialidad))

    conexion.commit()
    conexion.close()

def iniciar_sesion(correo, contrasena):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE correo = ? AND contrasena = ?", (correo, contrasena))
    usuario = cursor.fetchone()

    conexion.close()
    return usuario # Si existe, regresa los datos; si no, regresa None

def programar_tutoria(estudiante_id, tutor_id, fecha, hora, materia, estado="Programada"):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
       INSERT INTO tutorias (estudiante_id, tutor_id, fecha, hora, materia, estado)
       VALUES (?, ?, ?, ?, ?, ?)
    """, (estudiante_id, tutor_id, fecha, hora, materia, estado))
    conexion.commit()
    conexion.close()

def obtener_tutores():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, especialidad FROM usuarios WHERE tipo = 'tutor'")
    tutores = cursor.fetchall()
    conexion.close()
    return tutores

def obtener_tutorias_estudiante(estudiante_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT t.fecha, t.hora, u.nombre || ' ' || u.apellido AS tutor_nombre, t.materia, t.estado, t.motivo_cancelacion
        FROM tutorias t
        JOIN usuarios u ON t.tutor_id = u.id
        WHERE t.estudiante_id = ?
        ORDER BY t.fecha, t.hora
    """, (estudiante_id,))
    tutorias = cursor.fetchall()
    conexion.close()
    return tutorias

def cancelar_tutoria(fecha, hora, estudiante_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE tutorias
        SET estado = 'Cancelada'
        WHERE fecha = ? AND hora = ? AND estudiante_id = ?
    """, (fecha, hora, estudiante_id))
    conexion.commit()
    conexion.close()

def obtener_tutorias_tutor(tutor_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT t.fecha, t.hora, u.nombre || ' ' || u.apellido AS estudiante_nombre, t.materia, t.estado
        FROM tutorias t
        JOIN usuarios u ON t.estudiante_id = u.id
        WHERE t.tutor_id = ?
        ORDER BY t.fecha, t.hora
    """, (tutor_id,))
    tutorias = cursor.fetchall()
    conexion.close()
    return tutorias

def contar_tutorias_por_materia(estudiante_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT materia, COUNT(*) as cantidad
        FROM tutorias
        WHERE estudiante_id = ? AND estado = 'Programada'
        GROUP BY materia
    """, (estudiante_id,))
    datos = cursor.fetchall()
    conexion.close()
    return datos

def agregar_columna_motivo_cancelacion():
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("ALTER TABLE tutorias ADD COLUMN motivo_cancelacion TEXT")
        conexion.commit()
    except sqlite3.OperationalError:
        # Ya existe
        pass
    conexion.close

def cancelar_tutoria_por_tutor(fecha, hora, tutor_id, motivo):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE tutorias
        SET estado = 'Cancelada', motivo_cancelacion = ?
        WHERE fecha = ? AND hora = ? AND  tutor_id = ?
        """, (motivo, fecha, hora, tutor_id))
    conexion.commit()
    conexion.close()