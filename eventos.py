import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import conexion, variables, funcionescli, funcioneshab, funcionesreser, funcionesvar, facturacion, impresion,xlwt
import os, shutil
from datetime import date, datetime, time
class Eventos():

# eventos generales
    def on_acercade_activate(self, widget):
        """
        Abre la ventana de 'acerca de...'.

        Abre la ventana de informacion que tengamos
        asociada en el glade.

        :param widget:
        :return: void

        """

        try:
            variables.venacercade.show()
        except:
            print('error abrira acerca de')

    def on_btnCerrarabout_clicked(self, widget):
        """
        Cierra la ventana de 'acerca de...'.


        :param widget:
        :return: void

        """
        try:
            variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venacercade.hide()
        except:
            print('error abrir calendario')

    def on_menuBarsalir_activate(self, widget):
        """
        Llama al metodo salir() que finaliza la ejecucion del programa.

        Se activa con el click del botón finalizar
        de la barra de opciones, llamando a la función
        salir().

        :param widget:
        :return: void

        """
        try:
            self.salir()
        except:
            print('salir en menubar')

    def salir(self):
        """
        Finaliza la ejecucion del programa.

        Llama al metodo cerrarbbdd que cierra la base de datos
        y al metodo cerrartimer. Despues finaliza la ejecucion del programa.

        :return: void

        """

        try:
            conexion.Conexion.cerrarbbdd(self)
            funcionesvar.cerrartimer()
            Gtk.main_quit()
        except:
            print('error función salir')

    def on_venPrincipal_destroy(self, widget):
        """
        Llama al metodo salir() y finaliza la ejecucion del programa.

        Llama al metodo salir() para la finalización del
        programa cuando el usuario da un click sobre la cruz
        de cierre de la ventana.

        :param widget:
        :return: void

        """
        self.salir()

    def on_btnSalirtool_clicked(self, widget):
        """
        Abre la ventana de dialogo salir si/no.


        :param widget:
        :return: void
        """
        variables.vendialogsalir.show()

    def on_btnCancelarsalir_clicked(self, widget):
        """
        Cierra la ventana dialog salir.

        Se cierra la ventana al presionar el boton
        cancelar.

        :param widget:
        :return: void

        """
        variables.vendialogsalir.connect('delete-event', lambda w, e: w.hide() or True)
        variables.vendialogsalir.hide()

    def on_btnAceptarsalir_clicked(self, widget):
        """
        Llama al metodo salir() que finaliza el programa.

        Al presionar el boton aceptar de la ventana
        dialog salir, finaliza el programa por medio de
        la funcion salir().

        :param widget:
        :return:void

        """
        self.salir()
    """
    Eventos Clientes
    """

    def on_btnAltacli_clicked(self, widget):
        """
        Da de alta un cliente con los datos itroducidos en los entries.

        Llama a otro metodo para registrar los datos escritos
        en los entries de la ventana correspondientes, comprobando
        el dni por medio de otro método, insertando el cliente con la funcion
        insertarcli(), tambien borra los datos de los entries y actualiza los
        treeviews con otros dos metodos.

        :param widget:
        :return: void

        """

        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if funcionescli.validoDNI(dni):
                funcionescli.insertarcli(registro)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                variables.menslabel[0].set_text('ERROR DNI')
        except:
            print("Error alta cliente")



    def on_btnBajacli_clicked(self, widget):
        """
        Borra el cliente seleccionado en el treeview correspondiente.

        Recoje el dni en el entry del dni en la pestaña clientes
        que se puede meter a mano o dando click en uno de los clientes
        del treeview, y lo usa para borrar los datos del mismo para
        darle de baja.

        :param widget:
        :return: void

        """
        try:
            dni = variables.filacli[0].get_text()
            if dni != '' :
                funcionescli.bajacli(dni)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta dni u otro error')
        except:
            print("error en botón baja cliente")


    def on_btnModifcli_clicked(self, widget):
        """
        Modifica el cliente seleccionado con los datos introducidos en el entry.

        Modifica los datos del cliente almacenado despues de haber seleccionado
        en el treeview el caso a modificar. Una vez alterados los datos se vuelve
        a crear el treeview para actualizarlo con los datos introducidos y se limpia
        los datos de los entries.

        :param widget:
        :return: void

        """

        try:
            cod = variables.menslabel[1].get_text()
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != '':
                funcionescli.modifcli(registro, cod)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta el dni')
        except:
            print('error en botón modificar')



    def on_entDni_focus_out_event(self, widget, dni):
        #TODO
        """


        :param widget:
        :param dni:
        :return: void

        """
        try:
            dni = variables.filacli[0].get_text()
            if funcionescli.validoDNI(dni):
                variables.menslabel[0].set_text('')
                pass
            else:
                variables.menslabel[0].set_text('ERROR')
        except:
            print("Error alta cliente en out focus")


    def on_treeClientes_cursor_changed(self, widget):
        """
        Rellena los entries con los datos del cliente seleccionado en el treeView.

        :param widget:
        :return: void

        """
        try:
            model,iter = variables.treeclientes.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos
            variables.menslabel[0].set_text('')
            funcionescli.limpiarentry(variables.filacli)
            if iter != None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snome = model.get_value(iter, 2)
                sdata = model.get_value(iter, 3)
                if sdata == None:
                    sdata = ''
                cod = funcionescli.selectcli(sdni)
                variables.menslabel[1].set_text(str(cod[0]))
                variables.filacli[0].set_text(str(sdni))
                variables.filacli[1].set_text(str(sapel))
                variables.filacli[2].set_text(str(snome))
                variables.filacli[3].set_text(str(sdata))
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel))


        except:
            print ("error carga cliente")

    def on_btnCalendar_clicked(self, widget):
        """
        Abre el la ventana calendar.

        :param widget:
        :return: void

        """
        try:
            variables.semaforo = 1
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()

        except:
            print('error abrir calendario')

    def on_btnCalendarResIn_clicked(self,widget):
        #TODO
        """

        :param widget:
        :return:
        """
        try:
            variables.semaforo = 2
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_btnCalendarResOut_clicked(self, widget):
        #TODO
        """

        :param widget:
        :return:
        """
        try:
            variables.semaforo  = 3
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_Calendar_day_selected_double_click(self, widget):
        """
        Selecciona un dia del calendario para el entry y cierra la ventana del calendar.



        :param widget:
        :return: void

        """
        try:
            agno, mes, dia = variables.calendar.get_date()
            fecha = "%02d/" % dia + "%02d/" % (mes + 1) + "%s" % agno
            if variables.semaforo == 1:
                variables.filacli[3].set_text(fecha)
            elif variables.semaforo == 2:
                variables.filareserva[2].set_text(fecha)
            elif variables.semaforo == 3:
                variables.filareserva[3].set_text(fecha)
                funcionesreser.calculardias()
            else:
                pass
            #variables.semaforo = 0
            variables.vencalendar.hide()
        except:
            print('error al coger la fecha')

    def on_treeHab_cursor_changed(self, widget):
        """
        Introduce los datos de la habitacion elegida en el treeview en los entries.

        :param widget:
        :return: void

        """
        try:
            model, iter = variables.treehab.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos
            funcioneshab.limpiarentry(variables.filahab)
            if iter != None:
                snumhab = model.get_value(iter, 0)
                stipo = model.get_value(iter, 1)
                sprezo = model.get_value(iter, 2)
                sprezo = round(sprezo,2)
                variables.filahab[0].set_text(str(snumhab))
                variables.filahab[1].set_text(str(sprezo))
                if stipo == str('simple'):
                    variables.filarbt[0].set_active(True)
                elif stipo == str('doble'):
                    variables.filarbt[1].set_active(True)
                elif stipo == str('family'):
                    variables.filarbt[2].set_active(True)
                slibre = model.get_value(iter,3)
                if slibre == str('SI'):
                    variables.switch.set_active(True)
                else:
                    variables.switch.set_active(False)
        except:
            print("error carga habitacion")



    def on_btnAltahab_clicked(self, widget):
        """
        Da de alta una habitacion con los datos de los entries.

        Crea una nueva habitacion con los costes y el tipo introducido
        por medio de los entries, los radio buttons... y carga de nuevo
        el treeview borrando tambien los entries.

        :param widget:
        :return: void

        """
        try:
            numhab = variables.filahab[0].get_text()
            prezohab = variables.filahab[1].get_text()
            prezohab = prezohab.replace(',','.')
            prezohab = float(prezohab)
            prezohab = round(prezohab,2)
            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass

            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'
            registro = (numhab, tipo, prezohab, libre)
            if numhab != None:
               funcioneshab.insertarhab(registro)
               funcioneshab.listadohab(variables.listhab)
               funcioneshab.listadonumhab()
               funcioneshab.limpiarentry(variables.filahab)
            else:
                pass
        except:
            print("Error alta habitacion")




    def on_btnBajahab_clicked(self,widget):
        """
        Borra una habitacion seleccionada en el treeview.

        Elimina una habitacion del registro al seleccionarla
        en el treeview, limpia los entries y carga el treeview de nuevo.

        :param widget:
        :return: void

        """
        try:
            numhab = variables.filahab[0].get_text()
            if numhab != '':
                funcioneshab.bajahab(numhab)
                funcioneshab.limpiarentry(variables.filahab)
                funcioneshab.listadohab(variables.listhab)
            else:
                pass
        except:
            print('borrar baja hab')


    def on_btnModifhab_clicked(self, widget):
        """
        Modifica los datos de una habitacion seleccionada en el treeview.

        Modifica los datos de una habitacion seleccionada en el treeview
        cambiando los datos en los entries, al finalizar carga de nuevo el
        treeview y borra los entries.

        :param widget:
        :return: void

        """
        try:
            numhab = variables.filahab[0].get_text()
            prezo = variables.filahab[1].get_text()
            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'

            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass
            registro = (prezo, tipo, libre)
            if numhab != '':
                funcioneshab.modifhab(registro, numhab)
                funcioneshab.listadohab(variables.listhab)
                funcioneshab.limpiarentry(variables.filahab)
            else:
                print('falta el numhab')
        except:
            print('error modif hab')


    # eventos de los botones del toolbar

    def on_Panel_select_page(self, widget):
        """
        Recarga el treeview de habitaciones al cambiar de pestaña.
        :param widget:
        :return: void

        """
        try:
            funcioneshab.listadonumhab()
        except:
            print("error botón cliente barra herramientas")

    def on_btnClitool_clicked (self, widget):
        """

        :param widget:
        :return:
        """

        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                pass
        except:
            print("error botón cliente barra herramientas")

    def on_btnReservatool_clicked(self, widget):
        """
        Abre la pestaña de reservas y carga el treeview.

        :param widget:
        :return: void

        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 1:
                variables.panel.set_current_page(1)
                funcioneshab.listadonumhab(self)
            else:
                pass
        except:
            print("error botón cliente barra herramientas")

    def on_btnHabita_clicked(self,widget):
        """
        Abre la pestaña de habitaciones.

        :param widget:
        :return: void

        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                pass
        except:
            print("error botón habitacion barra herramientas")

    def on_btnCalc_clicked(self, widget):
        """
        Abre la calculadora del sistema operativo.

        :param widget:
        :return: void

        """
        try:
            os.system('/snap/bin/gnome-calculator')
        except:
            print('error lanzar calculadora')

    def on_btnRefresh_clicked(self, widget):
        """
        Vacia todos los entries.

        :param widget:
        :return:
        """
        try:
            funcioneshab.limpiarentry(variables.filahab)
            funcionescli.limpiarentry(variables.filacli)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesvar.limpiarlinfact(variables.linefactura)
        except:
            print('error referes')

    def on_btnBackup_clicked(self, widget):
        """
        Abre la ventana para seleccionar donde almacenar la copia de la bd.

        :param widget:
        :return: void

        """
        try:
            variables.filechooserbackup.show()
            variables.neobackup = funcionesvar.backup()
            variables.neobackup = str(os.path.abspath(variables.neobackup))
            print(variables.neobackup)

        except:
            print('error abrir file choorse backup')

    def on_btnGrabarbackup_clicked(self, widget):
        """
        Crea una copia de la base de datos por seguridad en el lugar seleccionado.

        :param widget:
        :return: void

        """

        try:
            destino = variables.filechooserbackup.get_filename()
            destino = destino + '/'
            variables.menslabel[3].set_text(str(destino))
            if shutil.move(str(variables.neobackup), str(destino)):
                variables.menslabel[3].set_text('Copia de Seguridad Creada')
        except:
            print('error dselect fichero')


    def on_btnCancelfilechooserbackup_clicked(self, widget):
        """
        Cierra la ventana de almacenar la copia de la base de datos sin guardar nada.

        :param widget:
        :return: void

        """
        try:
            variables.filechooserbackup.connect('delete-event', lambda w, e: w.hide() or True)
            variables.filechooserbackup.hide()
        except:
            print('error cerrar file chooser')


    def on_btnServicios_clicked(self, widget):

        """

        :param widget:
        :return:
        """

        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 3:
                variables.panel.set_current_page(3)
            else:
                pass
        except:
            print("error botón habitacion barra herramientas")


    def on_cmbNumres_changed(self, widget):
        try:
            index = variables.cmbhab.get_active()
            model = variables.cmbhab.get_model()
            item = model[index]
            variables.numhabres = item[0]
        except:
            print('error mostrar habitacion combo')

    def on_btnAltares_clicked(self, widget):
        """
        Crea una reserva de un cliente con una habitacion y su numero de noches.

        Define una nueva reserva con los datos del treeview clientes seleccionado
        y los datos que introduzcamos en los entries de la reserva, añadiendo
        la fecha de entrada, salida y la habitacion seleccionada. Recarga los
        treeviews y limpia los entries.

        :param widget:
        :return: void

        """
        try:
            if variables.reserva == 1:
                dnir = variables.menslabel[4].get_text()
                chki = variables.filareserva[2].get_text()
                chko = variables.filareserva[3].get_text()
                noches = int(variables.menslabel[2].get_text())
                registro = (dnir, variables.numhabres, chki, chko, noches)
                if funcionesreser.versilibre(variables.numhabres):
                    funcionesreser.insertares(registro)
                    funcionesreser.listadores()
                    #actualizar a NO
                    libre = ['NO']
                    funcioneshab.cambiaestadohab(libre, variables.numhabres)
                    funcioneshab.listadohab(variables.listhab)
                    funcioneshab.limpiarentry(variables.filahab)
                    funcionesreser.limpiarentry(variables.filareserva)
                else:
                    print ('habitación ocupada')
        except:
            print ('error en alta res')

    def on_btnRefreshcmbhab_clicked(self, widget):
        #TODO
        """

        :param widget:
        :return:
        """
        try:
            variables.cmbhab.set_active(-1)
            funcioneshab.listadonumhab(self)
        except:
            print ('error limpiar combo hotel')

    def on_treeReservas_cursor_changed(self, widget):
        """
        Selecciona los datos del treeView reservas, los mete en los entries y en la pestaña derecha

        :param widget:
        :return:void

        """
        try:
            model, iter = variables.treereservas.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos
            global snumhab
            funcionesreser.limpiarentry(variables.filareserva)
            if iter != None:
                variables.codr = model.get_value(iter,0)
                sdni = model.get_value(iter, 1)
                sapel = funcionesreser.buscarapelcli(str(sdni))
                snome = funcionesreser.buscarnome(str(sdni))
                snumhab =  model.get_value(iter, 2)
                lista = funcioneshab.listadonumhabres()
                m = -1
                for i, x in enumerate(lista):
                    if str(x[0]) == str(snumhab):
                        m = i
                variables.cmbhab.set_active(m)
                schki = model.get_value(iter, 3)
                schko = model.get_value(iter,4)
                snoches = model.get_value(iter, 5)
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel[0]))
                variables.menslabel[2].set_text(str(snoches))
                variables.filareserva[2].set_text(str(schki))
                variables.filareserva[3].set_text(str(schko))
                variables.mensfac[0].set_text(str(sdni))
                variables.mensfac[1].set_text(str(sapel[0]))
                variables.mensfac[2].set_text(str(variables.codr))
                variables.mensfac[3].set_text(str(snome[0]))
                variables.mensfac[4].set_text(str(snumhab))
                variables.mensserv[0].set_text(str(snumhab))
                variables.mensserv[1].set_text(str(variables.codr))
                global datosfactura
                datosfactura = (variables.codr, snoches, sdni, snumhab, schko)
                facturacion.cargargridfactura(datosfactura)
                funcionesvar.listaservicios(variables.listservicios)
                funcionesvar.limpiarlinfact(variables.linefactura)
                funcionesvar.cargalinefactura(variables.linefactura)
                funcionesvar.sumafactura(variables.codr, snoches, snumhab)

        except:
            print ('error cargar valores de reservas')


    def on_btnAnular_clicked(self, widget):

        try:
            libre = ['SI']
            numhabres = variables.numhabres
            funcionesreser.bajareserva(variables.codr)
            funcioneshab.cambiaestadohab(libre[0], numhabres)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesreser.listadores()
            funcioneshab.listadohab(variables.listhab)

        except:
            print('error baja reserva')

    def on_btnModifres_clicked(self, widget):
        try:
            dnir = variables.menslabel[4].get_text()
            chki = variables.filareserva[2].get_text()
            chko = variables.filareserva[3].get_text()
            noches = int(variables.menslabel[2].get_text())
            registro = (dnir, variables.numhabres, chki, chko, noches)
            funcionesreser.modifreserva(registro, variables.codr)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesreser.listadores()

        except:
            print('error modificar reserva')

    def on_btChkout_clicked(self, widget):
        try:
            chko = variables.filareserva[3].get_text()
            today = date.today()
            print(chko)
            hoy = datetime.strftime(today,'%d/%m/%Y')
            print(hoy)
            registro = (variables.numhabres)
            if str(hoy) == str(chko):
                funcioneshab.modifhabres(registro)
                funcioneshab.listadohab(variables.listhab)
            else:
                print('puede facturar')
                #cambiar el estado de la habitación de ocupada a libre

        except:
            print('error en checkout')

    def on_btnPrintfac_clicked(self, widget):
        """
        Llama a un metodo para imprimir la factura.

        :param widget:
        :return: void

        """
        try:
            impresion.factura(datosfactura)
        except Exception as e:
            print(e)



    """IMPORTAR EXPORTAR"""



    def on_exportar_activate(self,widget):
        """
        Abre la ventana del filechooser para exportar un elemento.

        :param widget:
        :return: void
        """
        try:
            variables.filechooserRutaExportar.show()
        except:
            print('Error openning file chooser')




    def on_importar_activate(self,widget):
        """
        Abre la ventana filechooser para importar un elemento.

        :param widget:
        :return: void
        """
        try:
            variables.filechooserRuta.show()
        except:
            print('Error openning file chooser')



    def on_btnelegirRutaExportarAceptar_clicked(self,widget):
        """
        Exporta a la carpeta indicada con el nombre de archivo indicado la bd.

        Comprueba que hayas introducido un nombre de  fichero y almacena
        el fichero exportado en la carpeta seleccionada con el nombre escrito.

        :param widget:
        :return: void
        """
        nombreFichero = variables.entryExportar.get_text()
        if(nombreFichero!=""):

            try:
                destino = variables.filechooserRutaExportar.get_filename()
                print(str(destino))


                 #Ejemplo de creación de hoja Excel
                 #definimos los estilos
                style0 = xlwt.easyxf('font: name DejaVu Sans')
                #Creamos un fichero excel
                wb = xlwt.Workbook()

                lista = funcionescli.listar()
                con=0
                # le añadimos una hoja llamada NuevoClientesque permite sobreescribir celdas
                ws = wb.add_sheet('NuevoClientes', cell_overwrite_ok=True)
                while con != len(lista):
                    # AQUÍ LO VAMOS RECORRIENDO E INSERTANDO EN LA CELDACORRESPONDIENTE
                    ws.write(con, 0, lista[con][1], style0)
                    ws.write(con, 1, lista[con][2], style0)
                    ws.write(con, 2, lista[con][3], style0)
                    ws.write(con, 3, lista[con][4], style0)
                    con=con + 1
                #Guardamos el archivo
                wb.save(destino+'/'+nombreFichero+'.xls')

            except Exception as e:
                print(e)
        else:
            print("No has metido na")

        variables.filechooserRutaExportar.connect('delete-event', lambda w, e: w.hide() or True)
        variables.filechooserRutaExportar.hide()




    def on_btnelegirRutaAceptar_clicked(self,widget):
        """
        Importa el archivo seleccionado en el filechooser.

        Importa el archivo que se haya seleccionado en el filechooser,
        lo introduce en la base de datos y actuliza los treeviews.
        Tambien cierra la ventana en cuestion.

        :param widget:
        :return: void
        """
        try:
            destino = variables.filechooserRuta.get_filename()
            print(str(destino))


            document = xlrd.open_workbook(str(destino))
            # Abrimos el fichero excel
            clientes = document.sheet_by_index(0)
            book_datemode = document.datemode
            for i in range(clientes.nrows - 1):
                # Ignoramos la primera fila, que indica los campos
                for j in range(clientes.ncols):
                    if i != 0:
                        if j == 0:
                            dni = str(clientes.cell_value(i, 0))
                            apel = str(clientes.cell_value(i, 1))
                            nome = str(clientes.cell_value(i, 2))
                            data = float(clientes.cell_value(i, 3))
                            year, mont, d, h, m, s = xlrd.xldate_as_tuple(data, 0)
                            dia = str(d)
                            mes = str(mont)
                            año = str(year)
                            fecha = dia.zfill(2) + '/' + mes.zfill(2) + '/' + año
                            registro = (dni, apel, nome, fecha)
                            if (funcionescli.selectcli(dni) == None):
                                funcionescli.insertarcli(registro)
                                funcionescli.listadocli(variables.listclientes)
                                funcionescli.limpiarentry(variables.filacli)

        except Exception as e:
            print(e)

        try:
            variables.filechooserRuta.connect('delete-event', lambda w, e: w.hide() or True)
            variables.filechooserRuta.hide()
        except:
            print('error cerrar file chooser')



    def on_btnelegirRutaExportarCancelar_clicked(self, widget):
        """
        Cierra la ventana filechooser de exportacion al pulsar cancelar.

        :param widget:
        :return: void
        """

        try:
            variables.filechooserRutaExportar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.filechooserRutaExportar.hide()
        except:
            print('error cerrar file chooser')


    def on_btnelegirRutaCancelar_clicked(self,widget):
        """
        Cierra la ventana filechooser de importacion al pulsar cancelar.

        :param widget:
        :return: void
        """

        try:
            variables.filechooserRuta.connect('delete-event', lambda w, e: w.hide() or True)
            variables.filechooserRuta.hide()
        except:
            print('error cerrar file chooser')



    """
    Gestión Prezos e Servizos 
    """


    def on_btnAltbasicos_clicked(self, widget):
        try:
            listaprecios = funcionesvar.preciosbasicos()
            tipo = funcionesvar.vertipohab(snumhab)
            noches = variables.menslabel[2].get_text()

            if str(tipo[0]) == 'simple':
                factor = 1.00
            elif str(tipo[0]) == 'doble':
                factor = 2.00
            elif str(tipo[0]) == 'family':
                factor = 3.00

            if variables.filarbtser[0].get_active():
                a = listaprecios[1].replace(',', '.')
                desayuno = float(factor) * float(a)
                desayuno = round(desayuno, 2)
                servicio = [variables.codr, 'Desayuno', desayuno]
                funcionesvar.altaserv(servicio)

            if variables.filarbtser[1].get_active():
                b = listaprecios[2].replace(',', '.')
                comida = float(factor) * float(b)
                comida = round(comida, 2)
                servicio = [variables.codr, 'Comida', comida]
                funcionesvar.altaserv(servicio)

            if variables.filarbtser[2].get_active():
                c = listaprecios[0].replace(',', '.')
                parking = float(noches) * float(c)
                parking = round(parking, 2)
                servicio = [variables.codr, 'Parking', parking]
                funcionesvar.altaserv(servicio)
            funcionesvar.listaservicios(variables.listservicios)
            funcionesvar.limpiarlinfact(variables.linefactura)
            funcionesvar.cargalinefactura(variables.linefactura)

        except:
            print('error en alta básicos')

    def on_etprezos_activate(self, widget):
        try:
            variables.venprezos.show()
            prezos = funcionesvar.mostrarprezos()
            for i in range(0,3):
                variables.prezos[i].set_text(prezos[i])
                variables.prezos[i].set_text(prezos[i])
                variables.prezos[i].set_text(prezos[i])
        except:
            print('error ventana prezos')

    def on_btnSalprezos_clicked(self, widget):
        try:
            variables.venprezos.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venprezos.hide()
        except:
            print('error ventana precios')

    def on_btnAltapre_clicked(self, widget):
        try:
            par = variables.prezos[0].get_text()
            des = variables.prezos[1].get_text()
            pc = variables.prezos[2].get_text()
            registro = (par, des, pc)
            funcionesvar.actualizarprezos(registro)
        except:
            print('error grabar boton prezos')



    def on_btnAltaotro_clicked(self, widget):
        try:
            otrobas = variables.otrobasico[0].get_text()
            prezobas = variables.otrobasico[1].get_text()
            prezobas = prezobas.replace(',', '.')
            prezobas = float(prezobas)
            prezobas = round(prezobas, 2)
            registro = (otrobas, prezobas)
            funcionesvar.altaotrobasico(registro, variables.codr)
            funcionesvar.listaservicios(variables.listservicios)
            funcionesvar.limpiarentservicios(variables.otrobasico)
            funcionesvar.limpiarlinfact(variables.linefactura)
            funcionesvar.cargalinefactura(variables.linefactura)

        except:
            print('error alta en otros básicos')

    def on_treeServicios_cursor_changed(self, wdiget):
        try:
            model, iter = variables.treeservicios.get_selection().get_selected()
            global codser
            if iter != None:
                codser = model.get_value(iter, 0)
                print(codser)
        except:
            print('error cargar servicios')


    def on_btnBajaser_clicked(self, widget):
        try:
            funcionesvar.bajaserv(codser)
            funcionesvar.listaservicios(variables.listservicios)
            funcionesvar.limpiarentservicios(variables.otrobasico)
            funcionesvar.limpiarlinfact(variables.linefactura)
            funcionesvar.cargalinefactura(variables.linefactura)
        except:
            print ('eliminar servicios')
