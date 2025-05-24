import customtkinter as ctk
from tkinter import messagebox
from backend import iniciar_sesion, crear_tablas,agregar_columna_motivo_cancelacion, registrar_usuario, Estudiante, Tutor, programar_tutoria, obtener_tutores, obtener_tutorias_estudiante, cancelar_tutoria, obtener_tutorias_tutor, contar_tutorias_por_materia, cancelar_tutoria_por_tutor
from tkcalendar import DateEntry
from PIL import Image
import matplotlib.pyplot as plt # type: ignore

# Crear tablas al iniciar
crear_tablas()
agregar_columna_motivo_cancelacion()

def ventana_inicio_sesion():
    app = ctk.CTk()
    app.iconbitmap("C://Users//Admin//Downloads//TutorUp//images//icon.ico")
    app.title("TutorUP - Inicio de Sesión")
    app.configure(fg_color= "#C4DCFF")
    app.geometry("400x660+479+28")

    #Imagen
    img = Image.open("C://Users//Admin//Downloads//TutorUp//images//login.png")
    ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(200,200))

    img_label = ctk.CTkLabel(app, image=ctk_image, text="")
    img_label.pack(pady=20)

    # Título
    titulo = ctk.CTkLabel(app, text="Iniciar Sesión ♡", font=ctk.CTkFont("Christmas Cookies", size= 40),text_color= "#2F4156")
    titulo.pack(pady=20)

    # Entrada de correo
    entry_correo = ctk.CTkEntry(app, width=300, height=35, placeholder_text="Ingresa tu correo", placeholder_text_color="#405367", corner_radius=10, fg_color="#7A95B1", font=ctk.CTkFont("Fruity Juice", size= 12))
    entry_correo.pack(pady=10)

    # Entrada de contraseña
    entry_contrasena = ctk.CTkEntry(app, width=300, height=35, placeholder_text="Ingresa tu contraseña", placeholder_text_color="#405367", corner_radius=10, fg_color="#7A95B1", font=ctk.CTkFont("Fruity Juice", size= 12), show="*")
    entry_contrasena.pack(pady=10)

    # Función login
    def login():
        correo = entry_correo.get()
        contrasena = entry_contrasena.get()

        usuario = iniciar_sesion(correo, contrasena)
        if usuario:
            tipo = usuario[1]
            nombre = usuario[2]
            messagebox.showinfo("Bienvenido!", f"Muy buenas {nombre} ({tipo})")

            if tipo == "estudiante":
                ventana_estudiante(usuario)
            elif tipo == "tutor":
                ventana_tutor(usuario)
        else:
            messagebox.showerror("Error", "Correo o Contraseña incorrectos")
    

    img1 = Image.open("C://Users//Admin//Downloads//TutorUp//images//deco1.png")
    ctk_image1 = ctk.CTkImage(light_image=img1, dark_image=img1, size= (140,140))

    img1_label = ctk.CTkLabel(app,text="", image=ctk_image1)
    img1_label.place(x=260, y=530)

    # Label de decoracion Estetica
    deco_label1 = ctk.CTkLabel(app, height=5, text="", fg_color="#C4DCFF")
    deco_label1.pack()

    # Botón de iniciar sesión
    btn_login = ctk.CTkButton(app,width=150, height= 30 , corner_radius=14, fg_color="#2B4A6A", text="Iniciar Sesión", command=login, font=ctk.CTkFont("Australia Custom", size= 20))
    btn_login.pack(pady=20)

    deco_label = ctk.CTkLabel(app, height=1, text="", fg_color="#C4DCFF")
    deco_label.pack()

    def ventana_registro():
        registro = ctk.CTkToplevel()
        registro.title("Registro de Usuario")
        registro.geometry("400x500")
        # Variables
        tipo_usuario = ctk.StringVar(value="estudiante")
        
        def alternar_campos():
            if tipo_usuario.get() == "estudiante":
                entry_materia.pack(pady=5)
                entry_especialidad.pack_forget()
            else:
                entry_materia.pack_forget()
                entry_especialidad.pack(pady=5)
                
        # Título
        ctk.CTkLabel(registro, text="Registrar Usuario", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Tipo de usuario (estudiante o tutor)
        ctk.CTkLabel(registro, text="Tipo de Usuario:").pack()
        ctk.CTkRadioButton(registro, text="Estudiante", variable=tipo_usuario, value="estudiante", command=alternar_campos).pack()
        ctk.CTkRadioButton(registro, text="Tutor", variable=tipo_usuario, value="tutor", command=alternar_campos).pack()

        # Datos comunes
        entry_nombre = ctk.CTkEntry(registro, placeholder_text="Nombre")
        entry_nombre.pack(pady=5)

        entry_apellido = ctk.CTkEntry(registro, placeholder_text="Apellido")
        entry_apellido.pack(pady=5)
        
        entry_correo = ctk.CTkEntry(registro, placeholder_text="Correo")
        entry_correo.pack(pady=5)
        
        entry_edad = ctk.CTkEntry(registro, placeholder_text="Edad")
        entry_edad.pack(pady=5)
        
        entry_contrasena = ctk.CTkEntry(registro, placeholder_text="Contraseña", show="*")
        entry_contrasena.pack(pady=5)
        
        # Campo para estudiante
        entry_materia = ctk.CTkEntry(registro, placeholder_text="Materia de Interes")
        
        # Campo para tutor
        entry_especialidad = ctk.CTkEntry(registro, placeholder_text="Especialidad")
        
        
        # Mostrar campos correctos por defecto
        alternar_campos()
        
        def registrar():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            edad = entry_edad.get()
            correo = entry_correo.get()
            contrasena = entry_contrasena.get()
            tipo = tipo_usuario.get()

            if tipo == "estudiante":
                materia = entry_materia.get()
                usuario = Estudiante(nombre, apellido, correo, contrasena, int(edad), materia)
            else:
                especialidad = entry_especialidad.get()
                if not especialidad:
                    messagebox.showerror("Error", "Especialidad requerida.")
                    return
                usuario = Tutor(nombre, apellido, correo, contrasena, int(edad), especialidad)

            try:
                registrar_usuario(usuario, tipo)
                messagebox.showinfo("Registro exitoso", f"{tipo.capitalize()} registrado correctamente")
                registro.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar: {e}")

        # Botón registrar
        ctk.CTkButton(registro, text="Registrar", command=registrar).pack(pady=10)

    # Botón de registro
    btn_registro = ctk.CTkButton(app, width=150, height= 30 , corner_radius=14, fg_color="#2B4A6A", text="Registrarse", command=lambda: ventana_registro(), font=ctk.CTkFont("Australia Custom", size= 20))
    btn_registro.pack()

    Label_dec = ctk.CTkLabel(app, width=400, height=14, fg_color="#7A95B1", text="")
    Label_dec.pack(pady=30)


    app.mainloop()

def ventana_programar_tutoria(usuario):
    programar = ctk.CTkToplevel()
    programar.title("Programar Tutoría")
    programar.geometry("400x500")

    ctk.CTkLabel(programar, text="Programar Tutoría", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

    # Obtener lista de tutores y mostrarla en un OptionMenu
    tutores = obtener_tutores()
    if not tutores:
        messagebox.showwarning("Sin tutores", "No hay tutores disponibles registrados.")
        programar.destroy()
        return

    # Diccionario: "Nombre (Especialidad)" -> ID
    opciones = {f"{t[1]} {t[2]} ({t[3]})": t[0] for t in tutores}
    tutor_nombres = list(opciones.keys())

    seleccion_tutor = ctk.StringVar(value=tutor_nombres[0])
    tutor_menu = ctk.CTkOptionMenu(programar, values=tutor_nombres, variable=seleccion_tutor)
    tutor_menu.pack(pady=5)

    ctk.CTkLabel(programar, text = "Selecciona una fecha:").pack(pady=5)
    calendario = DateEntry(programar, width=12, background= 'darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    calendario.pack(pady=5)

    entry_hora = ctk.CTkEntry(programar, placeholder_text="Hora (HH:MM)")
    entry_hora.pack(pady=5)

    def registrar_tutoria():
        tutor_id = opciones[seleccion_tutor.get()]
        fecha = calendario.get_date().strftime("%y-%m-%d")
        hora = entry_hora.get()
        materia = seleccion_tutor.get().split("(")[-1].replace(")", "").strip()
        estudiante_id = usuario[0]

        try:
            programar_tutoria(estudiante_id, tutor_id, fecha, hora, materia)
            messagebox.showinfo("Éxito", "Tutoría programada correctamente")
            programar.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al programar tutoría: {e}")

    ctk.CTkButton(programar, text="Programar Tutoría", command=registrar_tutoria).pack(pady=10)

def ventana_ver_tutorias(usuario):
    ventana = ctk.CTkToplevel()
    ventana.title("Mis Tutorías")
    ventana.geometry("600x400")

    ctk.CTkLabel(ventana, text="Mis Tutorías Agendadas", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

    tutorias = obtener_tutorias_estudiante(usuario[0])
    tutorias_programadas = [t for t in tutorias if t[4] == "Programada"]

    if not tutorias_programadas:
        ctk.CTkLabel(ventana, text="No tienes tutorías registradas.").pack(pady=20)
        return
    
    seleccion = ctk.StringVar(value="")

    opciones = [f"{t[0]} {t[1]} con {t[2]} - {t[3]}" for t in tutorias_programadas]
    menu = ctk.CTkOptionMenu(ventana, values=opciones, variable=seleccion)
    menu.pack(pady=10)

    def cancelar():
        if not seleccion.get():
            messagebox.showerror("Error", "Selecciona una tutoría para cancelar")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar esta tutoría?")
        if respuesta:
            # Obtener la fecha y hora de la tutoría seleccionada
            idx = opciones.index(seleccion.get())
            fecha, hora = tutorias_programadas[idx][0], tutorias_programadas[idx][1]
            cancelar_tutoria(fecha, hora, usuario[0])
            messagebox.showinfo("Cancelado", "Tutoría cancelada correctamente")
            ventana.destroy()

    ctk.CTkButton(ventana, text="Cancelar Tutoría", command=cancelar).pack(pady=10)

    # Encabezado tipo tabla
    encabezado = ctk.CTkLabel(ventana, text="Fecha | Hora | Tutor | Materia | Estado", anchor="w", justify="left")
    encabezado.pack(pady=5)

    # Mostrar cada tutoría
    for tutoria in tutorias:
        texto = f"{tutoria[0]} | {tutoria[1]} | {tutoria[2]} | {tutoria[3]} | {tutoria[4]}"
        if tutoria[4] == 'Cancelada' and tutoria[5]:
            texto += f" Motivo: {tutoria[5]}"
        ctk.CTkLabel(ventana, text=texto, anchor="w", justify="left").pack(anchor="w", padx=20)

def ventana_ver_tutorias_tutor(usuario):
    ventana = ctk.CTkToplevel()
    ventana.title("Mis Tutorías Asignadas")
    ventana.geometry("600x400")

    ctk.CTkLabel(ventana, text="Tutorías Asignadas", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

    tutorias = obtener_tutorias_tutor(usuario[0])

    if not tutorias:
        ctk.CTkLabel(ventana, text="No tienes tutorías registradas.").pack(pady=20)
        return

    encabezado = ctk.CTkLabel(ventana, text="Fecha | Hora | Estudiante | Materia | Estado", anchor="w", justify="left")
    encabezado.pack(pady=5)

    for tutoria in tutorias:
        texto = f"{tutoria[0]} | {tutoria[1]} | {tutoria[2]} | {tutoria[3]} | {tutoria[4]}"
        ctk.CTkLabel(ventana, text=texto, anchor="w", justify="left").pack(anchor="w", padx=20)

    ctk.CTkButton(ventana, text="Cancelar Tutoria", command= lambda: ventana_cancelar_tutoria_tutor(usuario)).pack(pady=5)

def ventana_grafica_estudiante(usuario):
    datos = contar_tutorias_por_materia(usuario[0])

    if not datos:
        messagebox.showinfo("Sin Datos", "No hay tutorias programadas para graficar.")
        return
    
    materias = [d[0] for d in datos]
    cantidades =  [d[1] for d in datos]

    plt.figure(figsize=(8, 5))
    plt.bar(materias, cantidades, color="skyblue")
    plt.title("Tutorias por Materia")
    plt.xlabel("Materias")
    plt.ylabel("Cantidad de Tutorias")
    plt.tight_layout()
    plt.show()

def ventana_cancelar_tutoria_tutor(usuario):
    ventana = ctk.CTkToplevel()
    ventana.title("Cancelar Tutoria")
    ventana.geometry("600x400")

    ctk.CTkLabel(ventana, text="Cancelar Tutoria Asignada", font=ctk.CTkFont(size=18,weight="bold")).pack(pady=10)

    tutorias = obtener_tutorias_tutor(usuario[0])
    tutorias_programadas = [t for t in tutorias if t[4] == "Programada"]

    if not tutorias_programadas:
        ctk.CTkLabel(ventana, text="No tienes tutorias prgramadas.").pack(pady=20)
        return
    
    seleccion = ctk.StringVar(value="")
    opciones = [f"{t[0]} {t[1]} con {t[2]} - {t[3]}" for t in tutorias_programadas]
    menu = ctk.CTkOptionMenu(ventana, values=opciones, variable=seleccion)
    menu.pack(pady=10)

    entry_motivo = ctk.CTkEntry(ventana, placeholder_text="Motivo de cancelacion")
    entry_motivo.pack(pady=10)

    def cancelar():
        if not seleccion.get():
            messagebox.showerror("Error", "Selecciona una tutoria para cancelar.")
            return
        motivo = entry_motivo.get()
        if not motivo:
            messagebox.showerror("Error", "Escribe un motivo de tu cancelacion.")
            return
        idx = opciones.index(seleccion.get())
        fecha, hora = tutorias_programadas[idx][0], tutorias_programadas[idx][1]
        cancelar_tutoria_por_tutor(fecha, hora, usuario[0], motivo)
        messagebox.showinfo("Cancelado", "Tutoria cancelada con exito!")
        ventana.destroy()
    ctk.CTkButton(ventana, text="Cancelar Tutoria", command=cancelar).pack(pady=10)

def ventana_estudiante(usuario):
    acciones = ctk.CTk()
    acciones.title("TutorUP - Panel del Estudiante")
    acciones.geometry("300x200+450+200")
    acciones.iconbitmap("C://Users//Admin//Downloads//TutorUp//images//icon.ico")

    ctk.CTkLabel(acciones, text = "Que quieres hacer?", font= ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

    ctk.CTkButton(acciones, text="Programar una Tutoria", command=lambda: ventana_programar_tutoria(usuario)).pack(pady=5)
    ctk.CTkButton(acciones, text="Ver mis Tutorias", command= lambda: ventana_ver_tutorias(usuario)).pack(pady=5)
    ctk.CTkButton(acciones, text="Ver grafica por materia", command= lambda: ventana_grafica_estudiante(usuario)).pack(pady=5)

    acciones.mainloop()

def ventana_tutor(usuario):
    acciones = ctk.CTk()
    acciones.title("TutorUP - Panel del Tutor")
    acciones.geometry("300x200+450+200")
    acciones.iconbitmap("C://Users//Admin//Downloads//TutorUp//images//icon.ico")

    ctk.CTkLabel(acciones, text="¿Qué deseas hacer?", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
    ctk.CTkButton(acciones, text="Ver mis Tutorías", command=lambda: ventana_ver_tutorias_tutor(usuario)).pack(pady=5)

    acciones.mainloop()

# Ejecutar la ventana
ventana_inicio_sesion()
