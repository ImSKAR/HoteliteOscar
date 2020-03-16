# coding=utf-8
import os, sqlite3

class Conexion:
    def abrirbbdd(self):
        """Abre una conexión a la base de datos.

        Abre una conexion a una base de datos de sqlite,
        en este caso a la de nombre empresa.

        :return: void

        Excepciones:

        """
        try:
            global bbdd, conex, cur
            bbdd = 'empresa.sqlite'         #variable que almacena la base de datos
            conex = sqlite3.connect(bbdd)   #la abrimos
            cur = conex.cursor()            #la variable cursor que hará las operaciones
            print("Conexión realizada correctamente")
        except sqlite3.OperationalError as e:
            print("Error al abrir: ", e)

    def cerrarbbdd(self):
        """Cierra una conexión a la base de datos.

        Cierra una conexion a una base de datos de sqlite
        e informa por terminal si se ha cerrado con éxito.

        :return: void

        Excepciones:

        """
        try:
            cur.close()
            conex.close()
            print("Base de datos cerrada correctamente ")
        except sqlite3.OperationalError as e:
            print("Error al cerrar: ", e)




