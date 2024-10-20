from fastapi import FastAPI, HTTPException,status
import mysql.connector
from core.connection import connection
from models.use import User
from models.loginp import LoginRequest
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.get('/')
def root():
    return {"message": "hola bienvenido"}


@app.get('/users')
def get_users():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios"

    try:
        cursor.execute(query)
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al conectar a MySQL: {err}")
    finally:
        cursor.close()


@app.post('/user')
def create_user(user: User):
    cursor = connection.cursor()
    query = """
    INSERT INTO usuarios (Nombre, Apellido, Email, Telefono, Password) 
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (user.Nombre, user.Apellido, user.Email, user.Telefono, user.Password)

    try:
        cursor.execute(query, values)
        connection.commit()
        return {"message": "Usuario creado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al guardar el usuario: {err}")
    except ValueError as e:
        raise HTTPException(status_code=403, detail=f"Error de validación: {e}")
    finally:
        cursor.close()


@app.put('/user/{user_id}')  # <-- Aquí está la corrección
def update_user(user_id: int, user: User):
    cursor = connection.cursor()
    query = """
    UPDATE usuarios 
    SET Nombre = %s, Apellido = %s, Email = %s, Telefono = %s, Password = %s
    WHERE UserId = %s
    """
    values = (user.Nombre, user.Apellido, user.Email, user.Telefono, user.Password, user_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario actualizado correctamente"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {err}")
    finally:
        cursor.close()


@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    cursor = connection.cursor()
    query = "DELETE FROM usuarios WHERE UserId = %s"

    try:
        cursor.execute(query, (user_id,))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"message": "Usuario eliminado correctamente"}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {err}")

    finally:
        cursor.close()




@app.post("/login")
def login_user(login_data: LoginRequest):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE Email = %s AND Password = %s"
    values = (login_data.Email, login_data.Password)

    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            return {"message": "Login correcto vale mia", "user": user}
        else:
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al conectar a MySQL: {err}")
    finally:
        cursor.close()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (cambia esto en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)


@app.post("/login")
def login_user(login_data: LoginRequest):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE Email = %s AND Password = %s"
    values = (login_data.Email, login_data.Password)

    try:
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            return {"message": "Login correcto vale mia ", "user": user}
        else:
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error al conectar a MySQL: {err}")
    finally:
        cursor.close()
