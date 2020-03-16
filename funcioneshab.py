"""
Aquí vendrán todas las funciones que afectan a la ¡gestión de los
habitaciones
Limpiarentry vaciará el contenido de los entry

"""

import conexion, sqlite3, variables

def insertarhab(fila):
    """
    Inserta un array con datos, obtenido por cabecera, en la base de datos.
    :param fila:
    :return: void
    """
    try:
        conexion.cur.execute('insert into habitacion(numero,tipo,prezo,libre) values(?,?,?,?)', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarhab():
    """
    Devuelve un array con todos los datos de las habitaciones.
    :return: Array
    """
    try:
        conexion.cur.execute('select * from habitacion')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarentry(fila):
    """
    Vacia los datos de las entries.
    :param fila:
    :return: void
    """
    for i in range(len(fila)):
        fila[i].set_text('')

def listadohab(listhab):
    """
    Carga los treeviews de habitaciones.

    :param listhab:
    :return: void
    """
    try:
        variables.listado = listarhab()
        variables.listhab.clear()
        for registro in variables.listado:
            listhab.append(registro)
    except:
        print("error en cargar treeview de hab")

def bajahab(numhab):
    """
    Borra una habitacion de la base de datos, gracias al numero pasado por cabecera.
    :param numhab:
    :return: void
    """
    try:
        conexion.cur.execute('delete from habitacion where numero = ?', (numhab,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifhab(registro, numhab):
    """
    Modifica una habitacion concreta.

    Modifica los datos de una habitacion concreta, que se buscar por
    el numero de habitacion pasado por cabecera y con el array que contiene los
    datos para modificar dicha habitacion.(registro)

    :param registro:
    :param numhab:
    :return:
    """
    try:
        conexion.cur.execute('update habitacion set tipo = ?, prezo = ?, libre = ? where numero = ?',
                             (registro[1], registro[0], registro[2], numhab))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadonumhab(self):
    """
    Carga el treeview de habitaciones.

    :param self:
    :return: void
    """
    try:
        conexion.cur.execute('select numero from habitacion')
        listado = conexion.cur.fetchall()
        variables.listcmbhab.clear()
        for row in listado:
            variables.listcmbhab.append(row)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def listadonumhabres():
    """
    Devuelve un array con los numeros de las habitaciones.

    :return: Array
    """
    try:
        conexion.cur.execute('select numero from habitacion')
        lista = conexion.cur.fetchall()
        return lista
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def cambiaestadohab(libre, numhabres):
    """
    Modifica el estado de la habitacion entre libre o ocupado.

    :param libre:
    :param numhabres:
    :return:
    """
    try:
        conexion.cur.execute('update habitacion set libre = ? where numero = ?',
                             (libre[0], numhabres))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
       print(e)
       conexion.conex.rollback()

def cargarprecio(numhab):
    """
    Carga el precio de una habitacion concreta definida por su numero desde la base de datos a un string.
    :param numhab:
    :return: String
    """
    try:
        conexion.cur.execute('select prezo from habitacion where numero = ?', (numhab,))
        prezo = conexion.cur.fetchone()
        return prezo

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifhabres(numhabres):
    """
    Vuelve una habitacion libre elegida por el numero de la misma y almacena contra la base de datos.
    :param numhabres:
    :return: void
    """
    try:
        libre = 'SI'
        conexion.cur.execute('update habitacion set libre = ? where numero = ?',
                             (libre, numhabres))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
       print(e)
       conexion.conex.rollback()