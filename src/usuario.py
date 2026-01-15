import bcrypt

def hash_clave(password_plana):
    # Generar un salt aleatorio
    salt = bcrypt.gensalt()
    # Hashear la contraseña (necesita estar en bytes)
    hashed = bcrypt.hashpw(password_plana.encode('utf-8'), salt)
    return hashed.decode('utf-8') # Guardamos como string en la BD

def check_clave(password_ingresada, hashed_guardado):
    # Comparamos la entrada con lo que tenemos en la base de datos
    return bcrypt.checkpw(
        password_ingresada.encode('utf-8'), 
        hashed_guardado.encode('utf-8')
    )
    
