import sqlite3
import os
from prettytable import PrettyTable

db = "Institucion.db"

"""------------------------------------------> FUNCIONES PRIMARIAS <-----------------------"""
def crear_base_datos():
    conexion = sqlite3.connect(db)
    cursor = conexion.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Curso (
        idCurso INTEGER PRIMARY KEY AUTOINCREMENT,
        materia TEXT NOT NULL,
        docente TEXT NOT NULL
    );
    """)
    print("Tabla 'Curso' creada correctamente.")


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Estudiante (
        idEstudiante INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        dni INTEGER NOT NULL UNIQUE,
        fecha_de_nacimiento TEXT NOT NULL,
        telefono INTEGER NOT NULL UNIQUE,
        direccion TEXT NOT NULL
    );
    """)
    print("Tabla 'Estudiante' creada correctamente.")


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Estudiante_Curso (
        idEstudiante INTEGER NOT NULL,
        idCurso INTEGER NOT NULL,
        PRIMARY KEY (idEstudiante, idCurso),
        FOREIGN KEY (idEstudiante) REFERENCES Estudiante(idEstudiante) ON DELETE CASCADE,
        FOREIGN KEY (idCurso) REFERENCES Curso(idCurso) ON DELETE CASCADE
    );
    """)
    print("Tabla 'Estudiante_Curso' creada correctamente.")


    conexion.commit()
    conexion.close()
    menu()

def menu():
    while True:
        print("\nMenú Principal:")
        print(" 1 --> Ingresar a un curso")
        print(" 2 --> Consultar datos")
        print(" 3 --> Eliminar datos")
        print(" 4 --> Ordenar datos")
        print(" 5 --> Modificar datos")
        print(" 6 --> Salir")
        
        try:
            valor = int(input("\nIngrese el valor deseado --> "))
            
            if valor == 1:
                Nuevo() 
            elif valor == 2:
                Consulta() 
            elif valor == 3:
                Eliminar()  
            elif valor == 4:
                Orden() 
            elif valor == 5:
                Modificar()  
            elif valor == 6:
                print("Saliendo del sistema... ¡Hasta luego!\n\n")
                exit()
            else:
                print("Opción inválida. Por favor, elija una opción del 1 al 6.")
        except ValueError:
            print("Error: Debe ingresar un número. Intente nuevamente.")
"""------------------------------------------> FUNCIONES SECUNDARIAS <-----------------------"""

def correccion():
    while True:
        corrector = input("¿Los datos están correctos? (s/n/salir) --> ").lower()
        if corrector == "s":
            return True
        elif corrector == "n":
            return False
        elif corrector == "salir":
            menu()
        else:
            print("Por favor, ingrese 's', 'n' o 'salir'.")

def Nuevo():
    conexion = sqlite3.connect(db)  
    cursor = conexion.cursor()
    while True:
        try:
            num = int(input("\nDesea agregar -->\n1-Materia \n2-Alumno \n3-Volver \n--> "))
            if num == 1:
                while True:
                    materia = input("\nIngrese la nueva materia --> ")
                    docente = input("Ingrese el docente --> ")
                    if correccion():
                        try:
                            cursor.execute("INSERT INTO Curso (materia, docente) VALUES (?, ?);", (materia, docente))
                            conexion.commit()
                            print("Nueva materia agregada correctamente.")
                            break
                        except sqlite3.IntegrityError as e:
                            print(f"Error al agregar la materia: {e}")
                    else:
                        print("Reingrese los datos de la materia.")

            elif num == 2:
                dni = int(input("\nIngrese el DNI del alumno --> "))
                
                cursor.execute("SELECT idEstudiante FROM Estudiante WHERE dni = ?;", (dni,))
                estudiante_existente = cursor.fetchone()

                if estudiante_existente:
                    print("El estudiante ya está registrado. \n")
                    id_estudiante = estudiante_existente[0]
                else:
                    print("Bienvenido nuevo estudiante :)  \n")
                    while True:
                        nombre = input("Ingrese el nombre del alumno --> ")
                        apellido = input("Ingrese el apellido del alumno --> ")
                        fecha_de_nacimiento = input("Ingrese la fecha de nacimiento (YYYY-MM-DD) --> ")
                        telefono = int(input("Ingrese el número de teléfono --> "))
                        direccion = input("Ingrese la dirección --> ")
                        if correccion():
                            cursor.execute("""
                                INSERT INTO Estudiante (nombre, apellido, dni, fecha_de_nacimiento, telefono, direccion)
                                VALUES (?, ?, ?, ?, ?, ?);
                            """, (nombre, apellido, dni, fecha_de_nacimiento, telefono, direccion))
                            conexion.commit()
                            id_estudiante = cursor.lastrowid  
                            break
                        else:
                            print("Reingrese los datos del estudiante.")


                cursor.execute("SELECT idCurso, materia, docente FROM Curso;")
                cursos = cursor.fetchall()
                if not cursos:
                    print("No hay cursos disponibles. Agregue uno primero.")
                    break

                print("Cursos disponibles:\n")
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Materia", "Docente"]
                for curso in cursos:
                    tabla.add_row([curso[0], curso[1], curso[2]])
                print(tabla)

                while True:
                    id_curso = int(input("\nSeleccione el ID del curso al que desea agregar al estudiante --> "))
                    if any(id_curso == curso[0] for curso in cursos):
                        if correccion():
                            try:
                                cursor.execute("INSERT INTO Estudiante_Curso (idEstudiante, idCurso) VALUES (?, ?);", (id_estudiante, id_curso))
                                conexion.commit()
                                print("Estudiante asociado correctamente al curso.")
                                break
                            except sqlite3.IntegrityError as e:
                                print(f"Error al asociar al estudiante con el curso: {e}")
                        else:
                            print("Reintente seleccionando el curso.")
                    else:
                        print("El ID ingresado no corresponde a ningún curso. Intente nuevamente.")

            elif num == 3:
                print("Volviendo al menú principal.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

        except ValueError:
            print("Por favor, ingrese un número válido.")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")

    conexion.close()

def Consulta():
    conexion = sqlite3.connect(db)
    cursor = conexion.cursor()
    while True:
        try:
            ingreso = int(input("\nDesea ver: \n1-Datos de un alumno \n2-Datos de un curso \n3-Volver \n--> "))
            if ingreso == 1:
                while True:
                    dni = int(input("\nIngrese el DNI del alumno --> "))
                    if correccion():
                        cursor.execute("SELECT * FROM Estudiante WHERE dni = ?;", (dni,))
                        alumno = cursor.fetchone()

                        if alumno:
                            tabla = PrettyTable()
                            tabla.field_names = ["ID Estudiante", "Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Teléfono", "Dirección"]
                            tabla.add_row([alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6]])
                            print("\nDatos del alumno:")
                            print(tabla)

                            cursor.execute("""
                                SELECT c.idCurso, c.materia, c.docente 
                                FROM Curso c
                                INNER JOIN Estudiante_Curso ec ON c.idCurso = ec.idCurso
                                WHERE ec.idEstudiante = ?;
                            """, (alumno[0],))
                            cursos = cursor.fetchall()

                            if cursos:
                                tabla_cursos = PrettyTable()
                                tabla_cursos.field_names = ["ID Curso", "Materia", "Docente"]
                                for curso in cursos:
                                    tabla_cursos.add_row([curso[0], curso[1], curso[2]])
                                print("\nCursos asociados:")
                                print(tabla_cursos)
                            else:
                                print("El alumno no está asociado a ningún curso.")
                            break
                        else:
                            print("No se encontró un alumno con el DNI ingresado. Intente nuevamente.")
                    else:
                        print("Vuelva a ingresar los datos")

            elif ingreso == 2:
                cursor.execute("SELECT * FROM Curso")
                cursos = cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ["ID Curso", "Materia", "Docente"]
                for curso in cursos:
                    tabla.add_row([curso[0], curso[1], curso[2]]) 
                print("\nTodos los cursos disponibles:")
                print(tabla)
                
                while True:

                    id_curso = int(input("\nIngrese el ID del curso --> "))
                    cursor.execute("SELECT * FROM Curso WHERE idCurso = ?;", (id_curso,))
                    curso = cursor.fetchone()

                    if curso:
                        tabla = PrettyTable()
                        tabla.field_names = ["ID Curso", "Materia", "Docente"]
                        tabla.add_row([curso[0], curso[1], curso[2]])
                        print("\nDatos del curso:")
                        print(tabla)

                        cursor.execute("""
                            SELECT e.idEstudiante, e.nombre, e.apellido, e.dni 
                            FROM Estudiante e
                            INNER JOIN Estudiante_Curso ec ON e.idEstudiante = ec.idEstudiante
                            WHERE ec.idCurso = ?;
                        """, (id_curso,))
                        estudiantes = cursor.fetchall()

                        if estudiantes:
                            tabla_estudiantes = PrettyTable()
                            tabla_estudiantes.field_names = ["ID Estudiante", "Nombre", "Apellido", "DNI"]
                            for estudiante in estudiantes:
                                tabla_estudiantes.add_row([estudiante[0], estudiante[1], estudiante[2], estudiante[3]])
                            print("\nEstudiantes asociados:")
                            print(tabla_estudiantes)
                        else:
                            print("No hay estudiantes asociados a este curso.")
                        break
                    else:
                        print("No se encontró un curso con el ID ingresado. Intente nuevamente.")

            elif ingreso == 3:
                print("Volviendo al menú principal.")
                menu()
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")

def Eliminar():
    conexion = sqlite3.connect(db)
    cursor = conexion.cursor()

    while True:
        try:
            ingreso = int(input("\n¿Qué desea realizar? \n1-Eliminar alumno \n2-Eliminar curso \n3-Volver \n--> "))
            
            if ingreso == 1: 
                while True:
                    dni = int(input("Ingrese el DNI del alumno que desea eliminar --> "))
                    cursor.execute("SELECT * FROM Estudiante WHERE dni = ?", (dni,))
                    estudiante = cursor.fetchone()

                    if estudiante:
                        cursor.execute("DELETE FROM Estudiante_Curso WHERE idEstudiante = ?", (estudiante[0],))
                        cursor.execute("DELETE FROM Estudiante WHERE dni = ?", (dni,))
                        conexion.commit()
                        print(f"El estudiante con DNI {dni} ha sido eliminado correctamente.")
                        break
                    else:
                        print("No se encontró un estudiante con ese DNI.")
                        reintentar = input("¿Desea intentar con otro DNI? (s/n) --> ").lower()
                        if reintentar != 's':
                            break

            elif ingreso == 2:  
                cursor.execute("SELECT * FROM Curso")
                cursos = cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ["ID Curso", "Materia", "Docente"]
                for curso in cursos:
                    tabla.add_row([curso[0], curso[1], curso[2]])  # Iterar sobre los cursos
                print("\nTodos los cursos disponibles:")
                print(tabla)
                while True:
                    id_curso = int(input("\nIngrese el ID del curso que desea eliminar --> "))
                    cursor.execute("SELECT * FROM Curso WHERE idCurso = ?", (id_curso,))
                    curso = cursor.fetchone()

                    if curso:
                        cursor.execute("DELETE FROM Estudiante_Curso WHERE idCurso = ?", (id_curso,))
                        cursor.execute("DELETE FROM Curso WHERE idCurso = ?", (id_curso,))
                        conexion.commit()
                        print(f"El curso con ID {id_curso} ha sido eliminado correctamente.")
                        break
                    else:
                        print("No se encontró un curso con ese ID.")
                        reintentar = input("¿Desea intentar con otro ID? (s/n) --> ").lower()
                        if reintentar != 's':
                            break

            elif ingreso == 3: 
                print("Volviendo al menú principal.")
                menu()

            else:
                print("Opción no válida. Intente nuevamente.")
        
        except ValueError:
            print("Por favor, ingrese un número válido.")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")

def Orden():
    conexion = sqlite3.connect(db)
    cursor = conexion.cursor()

    while True:
        try:
            consulta = int(input("\n¿Cómo desea ver los datos? \n1-Por ID \n2-Alumnos A-Z \n3-Alumnos Z-A \n4-Volver \n--> "))
            
            if consulta == 1:  
                cursor.execute("SELECT * FROM Estudiante ORDER BY idEstudiante;")
                estudiantes = cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Teléfono", "Dirección"]
                for estudiante in estudiantes:
                    tabla.add_row([estudiante[0], estudiante[1], estudiante[2], estudiante[3], estudiante[4], estudiante[5], estudiante[6]])
                print("\nEstudiantes ordenados por ID:")
                print(tabla)

            elif consulta == 2:  
                cursor.execute("SELECT * FROM Estudiante ORDER BY nombre;")
                estudiantes = cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Teléfono", "Dirección"]
                for estudiante in estudiantes:
                    tabla.add_row([estudiante[0], estudiante[1], estudiante[2], estudiante[3], estudiante[4], estudiante[5], estudiante[6]])
                print("\nEstudiantes ordenados por nombre (A-Z):")
                print(tabla)

            elif consulta == 3: 
                cursor.execute("SELECT * FROM Estudiante ORDER BY nombre DESC;")
                estudiantes = cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Teléfono", "Dirección"]
                for estudiante in estudiantes:
                    tabla.add_row([estudiante[0], estudiante[1], estudiante[2], estudiante[3], estudiante[4], estudiante[5], estudiante[6]])
                print("\nEstudiantes ordenados por nombre (Z-A):")
                print(tabla)

            elif consulta == 4: 
                print("Volviendo al menú principal.")
                break

            else:
                print("Opción no válida. Por favor, intente nuevamente.")

        except ValueError:
            print("Por favor, ingrese un número válido.")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")

def Modificar():
    conexion = sqlite3.connect(db)
    cursor = conexion.cursor()
    while True:
        try: 
            consulta = int(input("\n¿Qué desea modificar? \n1-Datos del Alumno \n2-Datos de Curso \n3-Volver\n--> "))
            
            if consulta == 1:  
                while True:
                    dni = int(input("\nIngrese el DNI del alumno que desea modificar --> "))
                    if correccion():
                        cursor.execute("SELECT * FROM Estudiante WHERE dni = ?;", (dni,))
                        alumno = cursor.fetchone()

                        if alumno:
                            tabla = PrettyTable()
                            tabla.field_names = ["ID Estudiante", "Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Teléfono", "Dirección"]
                            tabla.add_row([alumno[0], alumno[1], alumno[2], alumno[3], alumno[4], alumno[5], alumno[6]])
                            print("\nDatos actuales del alumno:")
                            print(tabla)

                            while True:
                                opcion = int(input("\n¿Qué dato desea modificar? \n1-Nombre \n2-Apellido \n3-DNI \n4-Fecha de Nacimiento \n5-Teléfono \n6-Dirección \n--> "))
                                
                                if opcion == 1:
                                    nuevo_nombre = input("\nIngrese el nuevo nombre --> ")
                                    cursor.execute("UPDATE Estudiante SET nombre = ? WHERE dni = ?;", (nuevo_nombre, dni))
                                
                                elif opcion == 2:
                                    nuevo_apellido = input("\nIngrese el nuevo apellido --> ")
                                    cursor.execute("UPDATE Estudiante SET apellido = ? WHERE dni = ?;", (nuevo_apellido, dni))
                                
                                elif opcion == 3:
                                    nuevo_dni = int(input("\nIngrese el nuevo DNI --> "))
                                    cursor.execute("UPDATE Estudiante SET dni = ? WHERE dni = ?;", (nuevo_dni, dni))
                                
                                elif opcion == 4:
                                    nueva_fecha = input("\nIngrese la nueva fecha de nacimiento (YYYY-MM-DD) --> ")
                                    cursor.execute("UPDATE Estudiante SET fecha_de_nacimiento = ? WHERE dni = ?;", (nueva_fecha, dni))
                                
                                elif opcion == 5:
                                    nuevo_telefono = int(input("\nIngrese el nuevo número de teléfono --> "))
                                    cursor.execute("UPDATE Estudiante SET telefono = ? WHERE dni = ?;", (nuevo_telefono, dni))
                                
                                elif opcion == 6:
                                    nueva_direccion = input("\nIngrese la nueva dirección --> ")
                                    cursor.execute("UPDATE Estudiante SET direccion = ? WHERE dni = ?;", (nueva_direccion, dni))
                                
                                else:
                                    print("\nOpción no válida.")
                                    

                                conexion.commit()
                                print("El dato ha sido modificado correctamente.")
                                menu()
                        else:
                            print("No se encontró un estudiante con ese DNI. Intente nuevamente.")

                    else: print("Vuelve a ingresar los datos")   

            elif consulta == 2:
                cursor.execute("SELECT * FROM Curso")
                cursos = cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ["ID Curso", "Materia", "Docente"]
                for curso in cursos:
                    tabla.add_row([curso[0], curso[1], curso[2]])  
                print("\nTodos los cursos disponibles:")
                print(tabla)
                while True:
                    id_curso = int(input("\nIngrese el ID del curso --> "))
                    cursor.execute("SELECT * FROM Curso WHERE idCurso = ?;", (id_curso,))
                    curso = cursor.fetchone()

                    if curso:
                        tabla = PrettyTable()
                        tabla.field_names = ["ID Curso", "Materia", "Docente"]
                        tabla.add_row([curso[0], curso[1], curso[2]])
                        print("\nDatos del curso:")
                        print(tabla)

                        while True:
                            opcion = int(input("\n¿Qué dato desea modificar? \n1-Materia \n2-Docente \n3-Volver \n--> "))
                            if opcion == 1:
                                nueva_materia= input("\nIngrese la nueva materia --> ")
                                cursor.execute("UPDATE Curso SET materia = ? WHERE idCurso = ?;", (nueva_materia , id_curso))
                            elif opcion == 2:
                                nuevo_docente= input("Ingrese el nuevo docente --> ")
                                cursor.execute("UPDATE Curso SET docente = ? WHERE idCurso = ?;", (nuevo_docente, id_curso))
                            elif opcion == 3:
                                Modificar()
                            else:
                                    print("Opción no válida.")
                            conexion.commit()
                            print("El dato ha sido modificado correctamente.")
                            menu()

                    else: print("ID ingresado es erroneo")
            
            elif consulta  ==  3: menu()

        except ValueError:
            print("Por favor, ingrese un número válido.")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")
    



"""------------------------------------------> INICIO Y VERIFICACION DE LA BASE<-----------------------"""

if not os.path.exists(db):
    print("Base de datos no encontrada...")
    while True:
        consulta = input("¿Desea crear una? (s/n): ")
        if consulta.lower() == "s":
            crear_base_datos()
        elif consulta.lower() == "n":
            print("Hasta luego :) ")
            exit()
        print("Dato erroneo")

else:
    print("Base de datos encontrada. \nBienvenido :) ")
    menu()
