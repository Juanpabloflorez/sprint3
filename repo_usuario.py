from typing import Optional, Dict
from firebase.config_firebase import FirebaseConfig
from firebase.usuario import Usuario
import firebase_admin
from firebase_admin import db, credentials
from view import view_consola


class UsuarioRepository:
    #repo para operaciones de Usuario en Firebase
    def __init__(self):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        self.ref = self.config.get_reference("Usuarios")
    
    def crear_usuario(self, user, pas):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")
        ref.child(user).set({"Password": pas, "Bees":0})

    def obtener_usuario(self, username: str) -> Optional[Dict]:
        try:
            return self.ref.child(username).get()
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
    
    def obtener_todos_usuarios(self) -> Optional[Dict]:
        try:
            return self.ref.get()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return None
    
    def validar_credenciales(self, username, password):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")

        resultado = ref.child(username).get()
        if password == resultado.get("Password"):
            view_consola.Loginview.Mostrarhome(self)
            view_consola.currentuser = username
        else:
            view_consola.Loginview.Mostrarincorrecto(self)