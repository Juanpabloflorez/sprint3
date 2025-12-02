from typing import Optional, Dict, Any
from firebase.config_firebase import FirebaseConfig
from firebase.tarea import Tarea
import firebase_admin
from firebase_admin import db, credentials
from view import view_consola
from model import repo_usuario


class TareaRepository:
    #repo para operaciones de Tarea en Firebase
    def __init__(self):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        self.usuarios_ref = self.config.get_reference("Usuarios")
    
    def agregar_tarea(self, user, nombre, tiempo, importancia, categoria):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")
        ref.child(user).child("Tareas").child(nombre).set({"Tiempo": tiempo, "Importancia": importancia, "Categoria": categoria, "Estado": False})
    
    def obtener_tareas(self, username, tarea):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")
        return ref.child(username).child("Tareas").child(tarea).get()
    
    def actualizar_nombre_tarea(self, user, name, newname):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")
        old = ref.child(user).child("Tareas").child(name)
        data = old.get()
        ref.child(user).child("Tareas").child(newname).set(data)
        old.delete()
    
    def actualizar_campo_tarea(self, user, nombre_tarea, opc, var):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")
        if opc == 2:
            ref.child(user).child("Tareas").child(nombre_tarea).update({"Tiempo": var})
        if opc == 3:
            ref.child(user).child("Tareas").child(nombre_tarea).update({"Importancia": var})
        if opc == 4:
            ref.child(user).child("Tareas").child(nombre_tarea).update({"Categoria": var})
    
    def eliminar_tarea(self, user, nombre):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")
        ref.child(user).child("Tareas").child(nombre).delete()

    def marcarcompleta(self, user, nombre):
        self.config = FirebaseConfig.get_instance()
        self.config.initialize()
        ref = db.reference("Usuarios")
        ref.child(user).child("Tareas").child(nombre).update({"Estado": True})
        ref.child(user).child("Tareas").child(nombre).delete()
        bee = db.reference(f"Usuarios/{user}")
        for unit, datos in bee:
            if unit == "Bees":
                datos += 1
                ref.child(user).update({"Bees": datos})