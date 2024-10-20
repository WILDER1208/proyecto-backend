from pydantic import BaseModel

class User(BaseModel):
    Nombre: str
    Apellido: str
    Email: str
    Telefono: str
    Password: str