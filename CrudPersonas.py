# Importamos los módulos
import sqlite3
from tkinter import *
from tkinter import messagebox


# Creamos la clase Persona
class Persona:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni


# Creamos la función conectar
def conectar():
    # Conectamos con la base de datos personas.db
    conexion = sqlite3.connect("personas.db")
    # Creamos el cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    # Creamos la tabla personas si no existe
    cursor.execute("CREATE TABLE IF NOT EXISTS personas (nombre TEXT, apellido TEXT,dni TEXT PRIMARY KEY)")
    # Confirmamos los cambios en la base de datos
    conexion.commit()
    # Cerramos la conexión
    conexion.close()


# Creamos la función insertar
def insertar(persona):
    # Conectamos con la base de datos personas.db
    conexion = sqlite3.connect("personas.db")
    # Creamos el cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    try:
        # Insertamos los datos de la persona en la tabla personas
        cursor.execute("INSERT INTO personas VALUES (?,?,?)", (persona.nombre, persona.apellido, persona.dni))
        # Confirmamos los cambios en la base de datos
        conexion.commit()
        # Mostramos un mensaje al usuario indicando el éxito
        messagebox.showinfo("Operación exitosa",
                            "Se ha insertado correctamente a " + persona.nombre + " " + persona.apellido)
        limpiar_campos()

    except sqlite3.IntegrityError:
        # Si ocurre un error al insertar por clave duplicada mostramos un mensaje al usuario indicando el fallo
        messagebox.showerror("Error", "Ya existe una persona con el DNI " + persona.dni)

    finally:
        # Cerramos la conexión
        conexion.close()




# Creamos la función consultar
def consultar(dni):
    # Conectamos con la base de datos personas.db
    conexion = sqlite3.connect("personas.db")
    # Creamos el cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    try:
        # Buscamos los datos de la persona por su DNI en la tabla personas
        cursor.execute("SELECT * FROM personas WHERE dni=?", (dni,))
        # Obtenemos el resultado como una tupla
        resultado = cursor.fetchone()
        if resultado is not None:
            # Si hay un resultado lo mostramos al usuario
            messagebox.showinfo("Consulta",
                                "Los datos de la persona son:\nNombre: " + resultado[0] + "\nApellido: " + resultado[1])

        else:
            # Si no hay un resultado mostramos un mensaje al usuario indicando que no se encontró a la persona
            messagebox.showerror("Error", "No se encontró a ninguna persona con el DNI " + dni)

        # except sqlite3.OperationalError:
        # # Si ocurre un error al consultar por una tabla inexistente mostramos un mensaje al usuario indicando el fallo
        # messagebox.showerror("Error", "La tabla personas no existe")

    finally:
        # Cerramos la conexión
        conexion.close()


# Creamos la función modificar
def modificar(persona):
    # Conectamos con la base de datos personas.db
    conexion = sqlite3.connect("personas.db")
    # Creamos el cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    try:
        # Actualizamos los datos de la persona por su DNI en la tabla personas
        cursor.execute("UPDATE personas SET nombre=?, apellido=? WHERE dni=?",
                       (persona.nombre, persona.apellido, persona.dni))
        # Confirmamos los cambios en la base de datos
        conexion.commit()
        if cursor.rowcount > 0:
            # Si hay filas afectadas mostramos un mensaje al usuario indicando el éxito
            messagebox.showinfo("Operación exitosa",
                                "Se ha modificado correctamente a " + persona.nombre + " " + persona.apellido)
            limpiar_campos()

        else:
            # Si no hay filas afectadas mostramos un mensaje al usuario indicando que no se encontró a la persona
            messagebox.showerror("Error", "No se encontró a ninguna persona con el DNI " + persona.dni)

    except sqlite3.OperationalError:
        # Si ocurre un error al modificar por una tabla inexistente mostramos un mensaje al usuario indicando el fallo
        messagebox.showerror("Error", "La tabla personas no existe")

    finally:
        # Cerramos la conexión
        conexion.close()


# Creamos la función eliminar
def eliminar(dni):
    # Conectamos con la base de datos personas.db
    conexion = sqlite3.connect("personas.db")
    # Creamos el cursor para ejecutar consultas SQL
    cursor = conexion.cursor()
    try:
        # Eliminamos los datos de la persona por su DNI en la tabla personas
        cursor.execute("DELETE FROM personas WHERE dni=?", (dni,))
        # Confirmamos los cambios en la base de datos
        conexion.commit()
        if cursor.rowcount > 0:
            # Si hay filas afectadas mostramos un mensaje al usuario indicando el éxito
            messagebox.showinfo("Operación exitosa", "Se ha eliminado correctamente a la persona con el DNI " + dni)
            limpiar_campos()

        else:
            # Si no hay filas afectadas mostramos un mensaje al usuario indicando que no se encontró a la persona
            messagebox.showerror("Error", "No se encontró a ninguna persona con el DNI " + dni)

    except sqlite3.OperationalError:
        # Si ocurre un error al eliminar por una tabla inexistente mostramos un mensaje al usuario indicando el fallo
        messagebox.showerror("Error", "La tabla personas no existe")

    finally:
        # Cerramos la conexión
        conexion.close()


# Creamos una ventana principal con tkinter
ventana = Tk()
ventana.title("CRUD de Personas")

# Creamos los widgets para ingresar los datos de las personas

# Etiqueta y entrada para el nombre
Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
nombre_entry = Entry(ventana)
nombre_entry.grid(row=0, column=1, padx=10, pady=10)

# Etiqueta y entrada para el apellido
Label(ventana, text="Apellido:").grid(row=1, column=0, padx=10, pady=10)
apellido_entry = Entry(ventana)
apellido_entry.grid(row=1, column=1, padx=10, pady=10)

# Etiqueta y entrada para el DNI
Label(ventana, text="DNI:").grid(row=2, column=0, padx=10, pady=10)
dni_entry = Entry(ventana)
dni_entry.grid(row=2, column=1, padx=10, pady=10)

# Creamos los botones para realizar las operaciones de CRUD

# Botón para insertar
boton_insertar = Button(ventana, text="Insertar",
                        command=lambda: insertar(Persona(nombre_entry.get(), apellido_entry.get(), dni_entry.get())))
boton_insertar.grid(row=3, column=0, padx=10, pady=10)

# Botón para consultar
boton_consultar = Button(ventana, text="Consultar", command=lambda: consultar(dni_entry.get()))
boton_consultar.grid(row=3, column=1, padx=10, pady=10)

# Botón para modificar
boton_modificar = Button(ventana, text="Modificar",
                         command=lambda: modificar(Persona(nombre_entry.get(), apellido_entry.get(), dni_entry.get())))
boton_modificar.grid(row=4, column=0, padx=10, pady=10)

# Botón para eliminar
boton_eliminar = Button(ventana, text="Eliminar", command=lambda: eliminar(dni_entry.get()))
boton_eliminar.grid(row=4, column=1, padx=10, pady=10)


def limpiar_campos():
    # Obtenemos las variables globales
    global nombre_entry, apellido_entry, dni_entry, nombre_label, apellido_label, dni_label

    # Limpiamos los valores de las cajas de texto
    nombre_entry.delete(0, END)
    apellido_entry.delete(0, END)
    dni_entry.delete(0, END)

    # Limpiamos los valores de los labels



# Ejecutamos la ventana principal
ventana.mainloop()
