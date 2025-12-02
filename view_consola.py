from typing import Optional, Dict
from viewmodel.usuario_viewmodel import UsuarioViewModel
from viewmodel.tarea_viewmodel import TareaViewModel
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from model import repo_usuario
from model import repo_tarea
import firebase_admin
from firebase_admin import db, credentials

global currentuser
currentuser = "e"
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Taskearly")
        self.geometry("600x300")

        # Contenedor donde estarán los frames
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Diccionario de frames
        self.frames = {}

        # Inicializar pantallas
        for F in (Mainview, Loginview, Crearview, Homeview, Agregarview, Quitarview, Editarview, Marcarcompletasview, Vertareasview):
            nombre = F.__name__
            frame = F(container, self)
            self.frames[nombre] = frame
            frame.place(relwidth=1, relheight=1)

        # Mostrar pantalla inicial
        self.mostrar_frame("Mainview")

    def mostrar_frame(self, nombre):
        frame = self.frames[nombre]
        frame.tkraise()

class Mainview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightblue")
        label = tk.Label(self, text="Taskearly", font=("Arial", 16))
        label.pack(pady=10)

        boton1 = tk.Button(self, text="Crear usuario", command=lambda: controller.mostrar_frame("Crearview"))
        boton1.place(x=260, y=90)

        boton2 = tk.Button(self, text="Iniciar sesión", command=lambda: controller.mostrar_frame("Loginview"))
        boton2.place(x=260, y=150)

class Crearview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightblue")
        self.controller = controller

        label = tk.Label(self, text="Crear usuario", font=("Arial", 16), bg="Blue")
        label.pack(pady=20)

        label = tk.Label(self, text="Usuario:", font=("Arial", 10))
        label.place(x=200, y=100)

        label = tk.Label(self, text="ID:", font=("Arial", 10))
        label.place(x=200, y=130)

        username = tk.Entry(self, textvariable=str, font=("Arial", 10))
        username.place(x=260, y=100)

        password = tk.Entry(self, textvariable=str, show="*")
        password.place(x=260, y=130)

        boton1 = tk.Button(self, text="Crear usuario", command=lambda: self.crear_usuario(username.get(),password.get()))
        boton1.place(x=260, y=160)

        volver = tk.Button(self, text="Volver", command=lambda: controller.mostrar_frame("Mainview"))
        volver.place(x=350, y=160)

    def crear_usuario(self, user, pas):
        repo_usuario.UsuarioRepository.crear_usuario(self,user,pas)
        global currentuser
        currentuser = user
        self.controller.mostrar_frame("Homeview")


class Loginview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="lightblue")
        self.controller = controller

        label = tk.Label(self, text="Iniciar sesion", font=("Arial", 16), bg="Blue")
        label.pack(pady=20)

        label = tk.Label(self, text="Usuario", font=("Arial", 10))
        label.place(x=200, y=100)

        label = tk.Label(self, text="ID", font=("Arial", 10))
        label.place(x=200, y=130)

        username = tk.Entry(self, textvariable=str, font=("Arial", 10))
        username.place(x=260, y=100)

        password = tk.Entry(self, textvariable=str, show="*")
        password.place(x=260, y=130)

        boton1 = tk.Button(self, text="Iniciar sesión", command=lambda: self.Hacerlogin(username.get(),password.get()))
        boton1.place(x=260, y=160)

        volver = tk.Button(self, text="Volver", command=lambda: controller.mostrar_frame("Mainview"))
        volver.place(x=350, y=160)

    def Hacerlogin(self,user,pas):
        repo_usuario.UsuarioRepository.validar_credenciales(self,user,pas)

    def Mostrarhome(self):
        self.controller.mostrar_frame("Homeview")

    def Mostrarincorrecto(self):
        label = tk.Label(self, text="Usuario o ID incorrectos", font=("Arial", 10), bg="Red")
        label.place(x=70, y=150)

class Homeview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Tareas Pendientes", font=("Arial", 16), bg="Lightblue")
        label.pack(pady=0, fill="x")

        agregar = tk.Button(self, text="Agregar Tareas", bg="lightgray", width=20, command=lambda: controller.mostrar_frame("Agregarview"))
        agregar.place(x=10, y=60)

        quitar = tk.Button(self, text="Quitar Tareas", bg="lightgray", width=20, command=lambda: controller.mostrar_frame("Quitarview"))
        quitar.place(x=10, y=90)

        editar = tk.Button(self, text="Editar Tareas", bg="lightgray", width=20, command=lambda: controller.mostrar_frame("Editarview"))
        editar.place(x=10, y=120)

        marcar = tk.Button(self, text="Marcar tareas completadas", bg="lightgray", width=20, command=lambda: controller.mostrar_frame("Marcarcompletasview"))
        marcar.place(x=10, y=150)

        config = tk.Button(self, text="Ver tareas", bg="lightgray", width=20, command=lambda: controller.mostrar_frame("Vertareasview"))
        config.place(x=10, y=180)

        volver = tk.Button(self, text="Cerrar Sesion", bg="lightgray", command=lambda: controller.mostrar_frame("Mainview"), background="Red")
        volver.place(x=20, y=270)

class Agregarview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Agregar Tarea", font=("Arial", 16), bg="Lightblue")
        label.pack(pady=0)

        name = tk.Label(self, text="Nombre:", font=("Arial", 10))
        name.place(x=120, y=60)

        time = tk.Label(self, text="Tiempo(Dias):", font=("Arial", 10))
        time.place(x=120, y=90)

        nombre = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
        nombre.place(x=210, y=60)

        tiempo = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
        tiempo.place(x=210, y=90)

        name = tk.Label(self, text="Importancia", font=("Arial", 10))
        name.place(x=20, y=60)

        opcion = tk.IntVar(value=0)
        opc1=tk.Radiobutton(self, text="Baja", variable=opcion, value=1)
        opc1.place(x=20, y=90)
        opc2=tk.Radiobutton(self, text="Media", variable=opcion, value=2)
        opc2.place(x=20, y=120)
        opc3=tk.Radiobutton(self, text="Alta", variable=opcion, value=3)
        opc3.place(x=20, y=150)

        name = tk.Label(self, text="Categoria", font=("Arial", 10))
        name.place(x=380, y=60)

        opcion2 = tk.IntVar(value=0)
        opc4=tk.Radiobutton(self, text="Estudio", variable=opcion2, value=1)
        opc4.place(x=380, y=90)
        opc5=tk.Radiobutton(self, text="Trabajo", variable=opcion2, value=2)
        opc5.place(x=380, y=120)
        opc6=tk.Radiobutton(self, text="Personal", variable=opcion2, value=3)
        opc6.place(x=380, y=150)

        agregar = tk.Button(self, text="Agregar Tarea", bg="lightgray", command=lambda: verificartiempo(self, currentuser, nombre.get(), tiempo.get(), opcion.get(), opcion2.get()))
        agregar.place(x=120, y=220)

        def verificartiempo(self, user, nombre, tiempo, opcion, opcion2):
                if not tiempo.isdigit():
                    messagebox.showerror("Editar tiempo","El tiempo en días debe ser un numero valido")
                else:
                    repo_tarea.TareaRepository.agregar_tarea(self, user, nombre, tiempo, opcion, opcion2)
                    controller.mostrar_frame("Homeview")

        volver = tk.Button(self, text="Volver a Home", bg="lightgray", command=lambda: controller.mostrar_frame("Homeview"))
        volver.place(x=220, y=220)

class Quitarview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Quitar Tarea", font=("Arial", 16), bg="Lightblue")
        label.pack(pady=0)

        name = tk.Label(self, text="Nombre", font=("Arial", 10))
        name.place(x=70, y=60)

        nombre = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
        nombre.place(x=120, y=60)

        global currentuser

        quitar = tk.Button(self, text="Quitar Tarea", bg="lightgray", command=lambda: repo_tarea.TareaRepository.eliminar_tarea(self, currentuser, nombre.get()))
        quitar.place(x=120, y=120)

        volver = tk.Button(self, text="Volver a Home", bg="lightgray", command=lambda: controller.mostrar_frame("Homeview"))
        volver.place(x=220, y=120)

class Editarview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Editar Tarea", font=("Arial", 16), bg="Lightblue")
        label.pack(pady=0)

        name = tk.Label(self, text="Nombre de la tarea:", font=("Arial", 10))
        name.place(x=40, y=40)

        tareaname = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
        tareaname.place(x=170, y=40)

        opcion = tk.IntVar(value=0)
        opc1=tk.Radiobutton(self, text="Editar Nombre", variable=opcion, value=1)
        opc1.place(x=70, y=90)
        opc2=tk.Radiobutton(self, text="Editar Tiempo", variable=opcion, value=2)
        opc2.place(x=70, y=120)
        opc3=tk.Radiobutton(self, text="Editar Importancia", variable=opcion, value=3)
        opc3.place(x=70, y=150)
        opc4=tk.Radiobutton(self, text="Editar Categoría", variable=opcion, value=4)
        opc4.place(x=70, y=180)

        global currentuser

        editar = tk.Button(self, text="Editar Tarea", bg="lightgray", command=lambda: self.Editartarea(currentuser, tareaname.get(), opcion.get(), controller))
        editar.place(x=70, y=210)

        volver = tk.Button(self, text="Volver a Home", bg="lightgray", command=lambda: controller.mostrar_frame("Homeview"))
        volver.place(x=170, y=210)

    def Editartarea(self,user,name,opc,controller):
        if opc == 1:
            newname = tk.Label(self, text="Nuevo nombre:", font=("Arial", 10))
            newname.place(x=220, y=90)

            nuevonombre = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
            nuevonombre.place(x=250, y=90)

            editar = tk.Button(self, text="Editar Nombre", bg="lightgray", command=lambda: (repo_tarea.TareaRepository.actualizar_nombre_tarea(self, user, name, nuevonombre.get()), controller.mostrar_frame("Homeview")))
            editar.place(x=250, y=110)

        if opc == 2:
            newname = tk.Label(self, text="Editar tiempo:", font=("Arial", 10))
            newname.place(x=250, y=90)

            var = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
            var.place(x=370, y=90)

            editar = tk.Button(self, text="Editar tiempo", bg="lightgray", command=lambda: verificartiempo(self, user, name, opc, var.get()))
            editar.place(x=370, y=130)

            def verificartiempo(self, user, name, opc, var):
                if not var.isdigit():
                    messagebox.showerror("Editar tiempo","El tiempo en días debe ser un numero valido")
                else:
                    repo_tarea.TareaRepository.actualizar_campo_tarea(self, user, name, opc, var.get())
                    controller.mostrar_frame("Homeview")

        if opc == 3:
            newname = tk.Label(self, text="Editar importancia:", font=("Arial", 10))
            newname.place(x=250, y=90)

            var = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
            var.place(x=370, y=90)

            editar = tk.Button(self, text="Editar importancia", bg="lightgray", command=lambda: (repo_tarea.TareaRepository.actualizar_campo_tarea(self, user, name, opc, var.get()), controller.mostrar_frame("Homeview")))
            editar.place(x=370, y=130)

        if opc == 4:
            newname = tk.Label(self, text="Editar categoria:", font=("Arial", 10))
            newname.place(x=250, y=90)

            var = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
            var.place(x=370, y=90)

            editar = tk.Button(self, text="Editar categoria", bg="lightgray", command=lambda: (repo_tarea.TareaRepository.actualizar_campo_tarea(self, user, name, opc, var.get()), controller.mostrar_frame("Homeview")))
            editar.place(x=370, y=130)

class Marcarcompletasview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Marcar tareas completas", font=("Arial", 16), bg="Lightblue")
        label.pack(pady=0)

        name = tk.Label(self, text="Nombre de la tarea", font=("Arial", 10))
        name.place(x=40, y=50)

        tareaname = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
        tareaname.place(x=180, y=50)

        global currentuser

        editar = tk.Button(self, text="Marcar tarea completa", bg="lightgray", command=lambda: (repo_tarea.TareaRepository.marcarcompleta(self, currentuser, tareaname.get()), controller.mostrar_frame("Homeview")))
        editar.place(x=150, y=110)

        volver = tk.Button(self, text="Volver a Home", bg="lightgray", command=lambda: controller.mostrar_frame("Homeview"))
        volver.place(x=300, y=110)

class Vertareasview(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Visor de tareas", font=("Arial", 16), bg="Lightblue")
        label.pack(pady=0)

        global currentuser

        editar = tk.Button(self, text="Ver tareas", bg="lightgray", command=lambda: (self.obtenertareas(currentuser)))
        editar.place(x=150, y=80)

        volver = tk.Button(self, text="Volver a Home", bg="lightgray", command=lambda: controller.mostrar_frame("Homeview"))
        volver.place(x=250, y=80)

        name = tk.Label(self, text="Buscar tarea por nombre: ", font=("Arial", 16), bg="Orange")
        name.place(x=350, y=80)

        buscartarea = tk.Entry(self, textvariable=tk.StringVar(), font=("Arial", 10))
        buscartarea.place(x=620, y=80)

        buscar = tk.Button(self, text="Buscar", bg="lightgray", command=lambda: (self.obtenertarea(buscartarea.get())))
        buscar.place(x=620, y=110)

        name = tk.Label(self, text="No olvides realizar estas tareas con poco tiempo: ", font=("Arial", 16), bg="Orange")
        name.place(x=150, y=40)

    def obtenertarea(self, name):
        label = tk.Label(self, text=repo_tarea.TareaRepository.obtener_tareas(self, currentuser, name), font=("Arial", 16), bg="Lightblue")
        label.place(x=800, y=80)

    def obtenertareas(self, user):
        ref = db.reference(f"Usuarios/{user}/Tareas")
        tareas = ref.get()
        fila = 170
        columnaurgente = 650

        for tarea, datos in tareas.items():
            name = tk.Label(self, text=tarea, font=("Arial", 16), bg="Lightblue")
            name.place(x=40, y=fila)
            label = tk.Label(self, text=repo_tarea.TareaRepository.obtener_tareas(self, user, tarea), font=("Arial", 16), bg="Lightblue")
            label.place(x=150, y=fila)
            tiempo = int(datos.get("Tiempo"))
            if tiempo == 2 or tiempo == 1 or tiempo == 0:
                tareaurgente = tk.Label(self, text=tarea, font=("Arial", 16), bg="Orange")
                tareaurgente.place(x=columnaurgente, y=40)
                columnaurgente += 100
            fila+=40