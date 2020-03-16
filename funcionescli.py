# coding=utf-8
"""Modulo que gestiona los clientes.
Este módulo contiene las funciones siguiente:
limpiarentry
Args:
    fila: contiene un listado de widgets de clientes que vamos a limpiar tras ejecutar un evento
    return:
    no devuelve nada

"""

import conexion
import sqlite3
import variables

def limpiarentry(fila):
    """
    Vacia los entries.

    :param fila:
    :return: void
    """

    variables.menslabel[1].set_text('')
    for i in range(len(fila)):
        fila[i].set_text('')

def validoDNI(dni):
    """
    Valida los DNIs.

    :param dni:
    :return: void
    """
    try:
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        dig_ext = "XYZ"
        reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
        numeros = "1234567890"
        dni = dni.upper()
        if len(dni) == 9:
            dig_control = dni[8]
            dni = dni[:8]
            if dni[0] in dig_ext:
                print(dni)
                dni = dni.replace(dni[0],reemp_dig_ext[dni[0]])
            return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control
        return False
    except:
        print("Error")
        return None


def insertarcli(fila):
    """
    Inserta un cliente en la base de datos.

    :param fila:
    :return: void;
    """
    try:
        conexion.cur.execute('insert into  clientes(dni,apel,nome, data) values(?,?,?,?)',fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def listar():
    """
    Devuelve un listado con los clientes.

    :return: array
    """
    try:
        conexion.cur.execute('select * from clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def bajacli(dni):
    """
    Borra un cliente de la base de datos.

    :param dni:
    :return: void
    """
    try:
        conexion.cur.execute('delete from clientes where dni = ?', (dni,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def modifcli(registro, cod):
    """
    Modifica un cliente en la base de datos.

    Altera las propiedades de un cliente y actualiza contra
    la base de datos.

    :param registro:
    :param cod:
    :return: void
    """
    try:
        conexion.cur.execute('update clientes set dni = ?, apel= ?, nome = ?, data = ? where id = ?',
                             (registro[0], registro[1], registro[2], registro[3], cod))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()



def listadocli(listclientes):
    """
    Carga el treeview de clientes.

    :param listclientes:
    :return: void
    """
    try:
        variables.listado = listar()
        listclientes.clear()
        for registro in variables.listado:
            listclientes.append(registro[1:5])
    except:
        print("error en cargar treeview")


def selectcli(dni):
    """
    Selecciona un cliente por medio de un dni pasado por cabecera.

    Usa el dni pasado por la cabecera para consultar un cliente
    concreto y devuelve todas las propiedades en forma de array.

    :param dni:
    :return: array
    """
    try:
        conexion.cur.execute('select id from clientes where dni = ?', (dni,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarentry(fila):
    """
    Vacia los entries.

    :param fila:
    :return: void
    """

    for i in range(len(fila)):
        fila[i].set_text('')

def apelnomfac(dni):
    """
    Saca de la base de datos el nombre y los apellidos de un cliente con un dni determinado.
    :param dni:
    :return: String
    """
    try:
        conexion.cur.execute('select apel, nome from clientes where dni = ?', (dni,))
        apelnome = conexion.cur.fetchone()
        conexion.conex.commit()
        return apelnome
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

