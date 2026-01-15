import psycopg2
import bcrypt
import pandas as pd
import numpy as np
import usuario as usr

# Configuración de la conexión
conn_params = {
    "host": "dpg-d5icubt6ubrc738hdg4g-a.frankfurt-postgres.render.com",
    "database": "dakar_kb_db",
    "user": "dakar_kb_db_user",
    "password": "VFq0OMkXPDZ8HgdQ5XuUKCmG7oPMSF17"
}

HOSTING = "dpg-d5icubt6ubrc738hdg4g-a.frankfurt-postgres.render.com"
PUERTO = "5432"
NOMBRE_DB = "dakar_kb_db"
USUARIO = "dakar_kb_db_user"
PSWD = "VFq0OMkXPDZ8HgdQ5XuUKCmG7oPMSF17"

def conexion(hosting, puerto, nombre_db, usuario, pswd):
        conn = psycopg2.connect(
                host = hosting,
                port = puerto,
                dbname = nombre_db,
                user = usuario,
                password = pswd
        )
        cursor = conn.cursor()
        return conn, cursor
    
def registrar_usuario(username, password_plana):
    # 1. Hashear la contraseña
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_plana.encode('utf-8'), salt).decode('utf-8')

    try:
        # 2. Conectar e insertar en Postgres
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)",
                    (username, password_hash)
                )
                conn.commit()
                
                print(f"Usuario '{username}' registrado con éxito.")
                
                return "OK"
    except Exception as e:
        print(f"Error al registrar: {e}")

def verificar_login(username, password_ingresada):
    try:
        # 1. Buscar el hash en la base de datos por el nombre de usuario
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT password_hash,id_usuario FROM usuarios WHERE username = %s",
                    (username,)
                )
                resultado = cur.fetchone()
                #print(resultado)

        if resultado:

            password_hash_db = resultado[0]
            # 2. Validar la contraseña ingresada contra el hash guardado
            if bcrypt.checkpw(password_ingresada.encode('utf-8'), password_hash_db.encode('utf-8')):
                print("Login exitoso.")
                return True, resultado[1]
            else:
                print("Contraseña incorrecta.")
                return False, resultado[1]
        else:
            print("El usuario no existe.")
            return False, None

    except Exception as e:
        print(f"Error en el login: {e}")
        return False,e
    
def sql_query_chats(usr):   # SELECT chat_session_id FROM chat_usuarios WHERE user_id == usr
    try:
        conex, cursor = conexion(HOSTING, PUERTO, NOMBRE_DB, USUARIO, PSWD)
        #query = f"SELECT DISTINCT chat_session_id FROM chat_usuarios WHERE user_id = {str(usr)}"
        query = f"SELECT id_chat, chat_session_id, pregunta_user, respuesta_user FROM chat_usuarios WHERE user_id = {str(usr)} ORDER BY id_chat DESC"
        #Si user_id es None, se guardará como NULL en Postgres.
        #print(query)
        cursor.execute(query)
        chats = cursor.fetchall()
        conex.close()
        
        return chats

    except Exception as e:
        return f"error: {e}" 
    
def sql_insert_chat(chat_id, user_id, pregunta, respuesta):
    try:
        conex, cursor = conexion(HOSTING, PUERTO, NOMBRE_DB, USUARIO, PSWD)
        query = """
            INSERT INTO chat_usuarios (chat_session_id, user_id, pregunta_user, respuesta_user)
            VALUES (%s, %s, %s, %s)
            """
        #Si user_id es None, se guardará como NULL en Postgres.
        cursor.execute(query, (chat_id, user_id, pregunta, respuesta))
        conex.commit()
        conex.close()
        return "OK"
    except Exception as e:
        return f"error: {e}" 