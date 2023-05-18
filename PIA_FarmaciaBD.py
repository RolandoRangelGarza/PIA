import mysql.connector
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import pandas as pd
import matplotlib.pyplot as plt

class farmacia_DB(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(r"C:\Users\wregi\OneDrive\Escritorio\PIA BD\PIA BD\PIA_Farmacia.ui", self)
        self.btn_regalm.clicked.connect(self.fn_registrar)
        self.btn_mostalm.clicked.connect(self.fn_refresh)
        self.btn_grafbar.clicked.connect(self.fn_graficaalm)

        self.btn_reglinprod.clicked.connect(self.fn_registrarlp)
        self.btn_mostlinprod.clicked.connect(self.fn_refreshlp)
        
        self.btn_regprod.clicked.connect(self.fn_registrarp)
        self.btn_mostprod.clicked.connect(self.fn_refreshp)

        self.btn_regalmprod.clicked.connect(self.fn_registraralp)
        self.btn_mostalmprod.clicked.connect(self.fn_refreshalp)
        self.btn_graf.clicked.connect(self.fn_graficaalp)

        self.btn_regclie.clicked.connect(self.fn_registrarcl)
        self.btn_mostclie.clicked.connect(self.fn_refreshcl)

        self.btn_regusua.clicked.connect(self.fn_registrarus)
        self.btn_mostusua.clicked.connect(self.fn_refreshus)

        self.btn_regtic.clicked.connect(self.fn_registrarti)
        self.btn_mosttic.clicked.connect(self.fn_refreshti)
        self.btn_vendi.clicked.connect(self.fn_vendiati)
        self.btn_grafven.clicked.connect(self.fn_grafrepti)
        # self.btn_grafven2.clicked.connect(self.grafcoti)

        

        self.btn_regdeta.clicked.connect(self.fn_registrardeti)
        self.btn_mostdeta.clicked.connect(self.fn_refreshdeti)

#-----------------------------------------TABLA ALMACEN-------------------------------------------------
    def fn_registrar(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clava = self.clave_alm.text()
        des = self.desc_alm.text()
        dire = self.dire_alm.text()
        enca = self.encar_alm.text()

        x = 0
        while x < 100:
            x += 0.0001
            self.progreso.setValue(int(x))

        sql = "INSERT INTO almacenes (id_almacen, descripcion, direccion, encargado) VALUES(%s, %s, %s, %s)"
        val = (clava, des, dire, enca)
        mycursor.execute(sql, val)
        self.clave_alm.clear()
        self.desc_alm.clear()
        self.dire_alm.clear()
        self.encar_alm.clear()
        self.clave_alm.setFocus()
        mydb.commit()

    
    def fn_refresh(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso.setValue(int(x))

        mycursor.execute("SELECT * FROM almacenes")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_almacenes.setRowCount(i)

        tablerow = 0
        for id_almacen, descripcion, direccion, encargado in datos:
            self.tbl_almacenes.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_almacen)))
            self.tbl_almacenes.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(descripcion))
            self.tbl_almacenes.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(direccion))
            self.tbl_almacenes.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(encargado))
            tablerow +=1
        mydb.commit()
        self.clave_alm.clear()
        self.desc_alm.clear()
        self.dire_alm.clear()
        self.encar_alm.clear()

    def fn_graficaalm(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso.setValue(int(x))

        mycursor = mydb.cursor()
        val = [self.clave_alm.text()]
        mycursor.execute("""SELECT almacenes_productos.id_almacen, almacenes_productos.id_producto, productos.descripcion,  almacenes_productos.cantidad\
                            FROM almacenes_productos \
                            INNER JOIN productos \
                            ON almacenes_productos.id_producto = productos.clave_producto \
                            WHERE almacenes_productos.id_almacen = %s \
                            ORDER BY cantidad ASC \
                            LIMIT 5""", (val))
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_b.setRowCount(i)

        tablerow = 0
        for id_almacen, id_producto, descripcion, cantidad in datos:
            self.tbl_b.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_almacen)))
            self.tbl_b.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(id_producto)))
            self.tbl_b.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(descripcion))
            self.tbl_b.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(cantidad)))
            tablerow +=1
        mydb.commit()

        columnHeaders = []

        # Create Columns Header List
        for j in range(self.tbl_b.columnCount()):
            columnHeaders.append(self.tbl_b.horizontalHeaderItem(j).text())
        df = pd.DataFrame(columns=columnHeaders)

        #create datafram object recordset
        for row in range(self.tbl_b.rowCount()):          
            for col in range(self.tbl_b.columnCount()):
                #var1 = self.tbl_b.item(row,col).text()
                #print(var1)
                df.at[row, columnHeaders[col]] = self.tbl_b.item(row,col).text()
        
        df.to_csv(r"C:\Users\wregi\OneDrive\Escritorio\PIA BD\PIA BD\vendidos.csv", index=False)

        data = pd.read_csv(r'C:\Users\wregi\OneDrive\Escritorio\PIA BD\PIA BD\vendidos.csv')
        df = pd.DataFrame(data,columns=['Nombre', 'Cantidad'])
        df.plot(x="Nombre", y= "Cantidad", kind="bar")
        plt.show()
#------------------------------FIN TABLA ALMACEN---------------------------------------

#-----------------------------------------TABLA LINEA PRODUCTO-------------------------------------------------
    def fn_registrarlp(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clavlp = self.clave_linprod.text()
        despl = self.desc_linprod.text()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_2.setValue(int(x))

        sql = "INSERT INTO lineas_productos (id_linea, Descripcion) VALUES(%s, %s)"
        val = (clavlp, despl)
        mycursor.execute(sql, val)
        self.clave_linprod.clear()
        self.desc_linprod.clear()
        self.clave_linprod.setFocus()
        mydb.commit()

    
    def fn_refreshlp(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_2.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM lineas_productos")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_linprod.setRowCount(i)

        tablerow = 0
        for id_linea, Descripcion in datos:
            self.tbl_linprod.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_linea)))
            self.tbl_linprod.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(Descripcion))
            tablerow +=1
        mydb.commit()
        self.clave_linprod.clear()
        self.desc_linprod.clear()

#------------------------------FIN TABLA LINEA PRODUCTO---------------------------------------


#-----------------------------------------TABLA PRODUCTO-------------------------------------------------
    def fn_registrarp(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clavp = self.clave_prod.text()
        clavplp = self.clave_linprod_prod.text()
        desp = self.desc_prod.text()
        unimed = self.unimed_prod.currentText()
        fechuc = self.fechulcomp_prod.text()
        prec = self.precio_prod.text()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_3.setValue(int(x))

        sql = "INSERT INTO productos (clave_producto, clave_linea, descripcion, Unidad_medida, fecha_ult_compra, precio) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (clavp, clavplp, desp, unimed, fechuc, prec)
        mycursor.execute(sql, val)
        self.clave_prod.clear()
        self.clave_linprod_prod.clear()
        self.desc_prod.clear()
        self.unimed_prod.clear()
        self.fechulcomp_prod.clear()
        self.precio_prod.clear()
        self.clave_prod.setFocus()
        mydb.commit()

    
    def fn_refreshp(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_3.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM productos")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_prod.setRowCount(i)

        tablerow = 0
        for clave_producto, clave_linea, descripcion, Unidad_medida, fecha_ult_compra, precio in datos:
            self.tbl_prod.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(clave_producto)))
            self.tbl_prod.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(clave_linea)))
            self.tbl_prod.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(descripcion))
            self.tbl_prod.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(Unidad_medida))
            self.tbl_prod.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(fecha_ult_compra)))
            self.tbl_prod.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(precio)))
            tablerow +=1
        mydb.commit()
        self.clave_prod.clear()
        self.clave_linprod_prod.clear()
        self.desc_prod.clear()
        self.unimed_prod.clear()
        self.fechulcomp_prod.clear()
        self.precio_prod.clear()
        self.clave_prod.setFocus()

#------------------------------FIN TABLA PRODUCTO---------------------------------------


#-----------------------------------------TABLA ALMACEN_PRODUCTO-------------------------------------------------
    def fn_registraralp(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clavap = self.clave_alm_almprod.text()
        clavpap = self.clave_prod_almprod.text()
        cantap = self.cant_almprod.text()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_4.setValue(int(x))

        sql = "INSERT INTO almacenes_productos (id_almacen, id_producto, cantidad) VALUES(%s, %s, %s)"
        val = (clavap, clavpap, cantap)
        mycursor.execute(sql, val)
        self.clave_alm_almprod.clear()
        self.clave_prod_almprod.clear()
        self.cant_almprod.clear()
        self.clave_alm_almprod.setFocus()
        mydb.commit()

    
    def fn_refreshalp(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_4.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT almacenes_productos.id_almacen, almacenes_productos.id_producto, productos.descripcion, almacenes_productos.cantidad \
                            FROM almacenes_productos \
                            INNER JOIN productos \
                            ON almacenes_productos.id_producto = productos.clave_producto ORDER BY id_almacen;")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_almprod.setRowCount(i)

        tablerow = 0
        for id_almacen, id_producto, descripcion, cantidad in datos:
            self.tbl_almprod.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_almacen)))
            self.tbl_almprod.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(id_producto)))
            self.tbl_almprod.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(descripcion))
            self.tbl_almprod.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(cantidad)))
            tablerow +=1
        mydb.commit()
        self.clave_alm_almprod.clear()
        self.clave_prod_almprod.clear()
        self.cant_almprod.clear()
        self.clave_alm_almprod.setFocus()

    def fn_graficaalp(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_4.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT almacenes_productos.id_almacen, sum(almacenes_productos.cantidad * productos.precio) as costo \
                            from almacenes_productos, productos \
                            where almacenes_productos.id_producto = productos.clave_producto \
                            group by id_almacen;")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_c.setRowCount(i)

        tablerow = 0
        for id_almacen, costo in datos:
            self.tbl_c.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_almacen)))
            self.tbl_c.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(costo)))
            tablerow +=1
        mydb.commit()

        columnHeaders = []

        # Create Columns Header List
        for j in range(self.tbl_c.columnCount()):
            columnHeaders.append(self.tbl_c.horizontalHeaderItem(j).text())
        df = pd.DataFrame(columns=columnHeaders)

        #create datafram object recordset
        for row in range(self.tbl_c.rowCount()):          
            for col in range(self.tbl_c.columnCount()):
                df.at[row, columnHeaders[col]] = self.tbl_c.item(row,col).text()
        
        df.to_csv(r"C:\Users\wregi\OneDrive\Escritorio\PIA BD\PIA BD\inventario.csv", index=False)

        data = pd.read_csv(r'C:\Users\wregi\OneDrive\Escritorio\PIA BD\PIA BD\inventario.csv')
        df_reset=data.set_index('Almacen')
        df = pd.DataFrame(df_reset,columns=['Almacen', 'Costo'])
        df.plot(x="Almacen", y= "Costo", kind="pie", autopct='%0.0f%%')
        i = 0.4
        ii= 0.3
        for id_almacen, costo in datos:
            plt.text(1.2,i,"El almacen" + " " + str(id_almacen), fontsize=10)
            plt.text(1.2,ii,"sus costo es de" + " " + str(costo), fontsize=10)
            i+=0.2
            ii+=0.2
        plt.show()

#------------------------------FIN TABLA ALMACEN_PRODUCTO---------------------------------------


#-----------------------------------------TABLA CLIENTE-------------------------------------------------
    def fn_registrarcl(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clavcl = self.clave_clie.text()
        nombcl = self.nom_clie.text()
        dircl = self.dire_clie.text()
        corcl = self.corr_clie.text()
        telcl = self.tel_clie.text()
        limcl = self.limcred_clie.text()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_5.setValue(int(x))
        sql = "INSERT INTO clientes (id_cliente, nombre, direccion, correo, telefono, limite_credito) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (clavcl, nombcl, dircl, corcl, telcl, limcl)
        mycursor.execute(sql, val)
        self.clave_clie.clear()
        self.nom_clie.clear()
        self.dire_clie.clear()
        self.corr_clie.clear()
        self.tel_clie.clear()
        self.limcred_clie.clear()
        self.clave_clie.setFocus()
        mydb.commit()

    
    def fn_refreshcl(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_5.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id_cliente, nombre, direccion, correo, telefono, limite_credito FROM clientes")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_clie.setRowCount(i)

        tablerow = 0
        for id_cliente, nombre, direccion, correo, telefono, limite_credito in datos:
            self.tbl_clie.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_cliente)))
            self.tbl_clie.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(nombre))
            self.tbl_clie.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(direccion))
            self.tbl_clie.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(correo))
            self.tbl_clie.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(telefono))
            self.tbl_clie.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(limite_credito)))
            tablerow +=1
        mydb.commit()
        self.clave_clie.clear()
        self.nom_clie.clear()
        self.dire_clie.clear()
        self.corr_clie.clear()
        self.tel_clie.clear()
        self.limcred_clie.clear()
        self.clave_clie.setFocus()

#------------------------------FIN TABLA CLIENTE---------------------------------------


#-----------------------------------------TABLA USUARIOS-------------------------------------------------
    def fn_registrarus(self):
        mydb = mysql.connector.connect(
       host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clavus = self.clave_usua.text()
        conus = self.contra_usua.text()
        nomus = self.nom_usua.text()
        if self.tipo_usuaC.isChecked():
            tipus = "Cajero"
        elif self.tipo_usuaV.isChecked():
            tipus = "Vendedor"
        elif self.tipo_usuaG.isChecked():
            tipus = "Gerente"
        corrus = self.corr_usua.text()
        telus = self.tel_usua.text()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_6.setValue(int(x))

        sql = "INSERT INTO usuarios_sistema (clave_usuario, contrasena, nombre, tipo, correo, telefono) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (clavus, conus, nomus, tipus, corrus, telus)
        mycursor.execute(sql, val)
        self.clave_usua.clear()
        self.contra_usua.clear()
        self.nom_usua.clear()
        self.corr_usua.clear()
        self.tel_usua.clear()
        self.clave_usua.setFocus()
        mydb.commit()

    
    def fn_refreshus(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_6.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM usuarios_sistema")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_usua.setRowCount(i)

        tablerow = 0
        for clave_usuario, contrasena, nombre, tipo, correo, telefono in datos:
            self.tbl_usua.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(clave_usuario)))
            self.tbl_usua.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(contrasena))
            self.tbl_usua.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(nombre))
            self.tbl_usua.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(tipo))
            self.tbl_usua.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(correo))
            self.tbl_usua.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(telefono))
            tablerow +=1
        mydb.commit()
        self.clave_usua.clear()
        self.contra_usua.clear()
        self.nom_usua.clear()
        self.corr_usua.clear()
        self.tel_usua.clear()
        self.clave_usua.setFocus()

#------------------------------FIN TABLA USUARIOS---------------------------------------


#-----------------------------------------TABLA TICKET-------------------------------------------------
    def fn_registrarti(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clavti = self.clave_tic.text()
        clavusti = self.clave_usua_tic.text()
        clavclti = self.clave_clie_tic.text()
        fecti = self.fech_tic.text()
        sucuti = self.sucur_tic.text()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_7.setValue(int(x))
        sql = "INSERT INTO tickets (id_ticket, id_usuario, id_cliente, fecha, sucursal) VALUES(%s, %s, %s, %s, %s)"
        val = (clavti, clavusti, clavclti, fecti, sucuti)
        mycursor.execute(sql, val)
        self.clave_tic.clear()
        self.clave_usua_tic.clear()
        self.clave_clie_tic.clear()
        self.fech_tic.clear()
        self.sucur_tic.clear()
        self.clave_tic.setFocus()
        mydb.commit()

    
    def fn_refreshti(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_7.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM tickets")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tb_tic.setRowCount(i)

        tablerow = 0
        for id_ticket, id_usuario, id_cliente, fecha, sucursal in datos:
            self.tb_tic.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_ticket)))
            self.tb_tic.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(id_usuario)))
            self.tb_tic.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(id_cliente)))
            self.tb_tic.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(fecha)))
            self.tb_tic.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(sucursal))
            tablerow +=1
        mydb.commit()
        self.clave_tic.clear()
        self.clave_usua_tic.clear()
        self.clave_clie_tic.clear()
        self.fech_tic.clear()
        self.sucur_tic.clear()
        self.clave_tic.setFocus()

    def fn_vendiati(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_7.setValue(int(x))
        mycursor = mydb.cursor()
        val = [self.fech_tic.text()]
        mycursor.execute("""SELECT t.fecha, SUM((p.precio * dt.cantidad)) AS 'TOTAL' \
                        FROM detalles_tickets AS dt \
                        INNER JOIN tickets AS t ON dt.id_ticket = t.id_ticket \
                        INNER JOIN productos AS p ON dt.clave_producto = p.clave_producto \
                        WHERE t.fecha = %s""", (val))
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_vendi.setRowCount(i)

        tablerow = 0
        for fecha, TOTAL in datos:
            self.tbl_vendi.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(fecha)))
            self.tbl_vendi.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(TOTAL)))
            tablerow +=1
        mydb.commit()
        for row in range(self.tbl_vendi.rowCount()):
            self.vendi.setText(self.tbl_vendi.item(row,1).text())

    
    def fn_grafrepti(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_7.setValue(int(x))
        mycursor = mydb.cursor()
        val1 = self.fech_tic.text()
        val2 = self.fech_tic2.text()
        mycursor.execute("""SELECT t.fecha, SUM((p.precio * dt.cantidad)) AS 'TOTAL'\
                            FROM detalles_tickets AS dt \
                            INNER JOIN tickets AS t ON dt.id_ticket = t.id_ticket \
                            INNER JOIN productos AS p ON dt.clave_producto = p.clave_producto \
                            WHERE t.fecha BETWEEN %s AND %s \
                            GROUP BY t.fecha""", (val1, val2))
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_vendi2.setRowCount(i)

        tablerow = 0
        for fecha, TOTAL in datos:
            self.tbl_vendi2.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(fecha)))
            self.tbl_vendi2.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(TOTAL)))
            tablerow +=1
        mydb.commit()

        columnHeaders = []

        # Create Columns Header List
        for j in range(self.tbl_vendi2.columnCount()):
            columnHeaders.append(self.tbl_vendi2.horizontalHeaderItem(j).text())
        df = pd.DataFrame(columns=columnHeaders)

        #create datafram object recordset
        for row in range(self.tbl_vendi2.rowCount()):          
            for col in range(self.tbl_vendi2.columnCount()):
                df.at[row, columnHeaders[col]] = self.tbl_vendi2.item(row,col).text()
        
        df.to_csv(r"C:\Users\wregi\OneDrive\Escritorio\PIA BD\PIA BD\vendias.csv", index=False)

        data = pd.read_csv(r'C:\Users\wregi\OneDrive\Escritorio\PIA BD\PIA BD\vendias.csv')
        df = pd.DataFrame(data,columns=['Fecha', 'TOTAL'])
        df.plot(x="Fecha", y= "TOTAL")
        plt.show()
    
    def grafcoti(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_4.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT almacenes_productos.id_almacen, sum(almacenes_productos.cantidad * productos.precio) as costo \
                            from almacenes_productos, productos \
                            where almacenes_productos.id_producto = productos.clave_producto \
                            group by id_almacen;")
        datos = mycursor.fetchall()
        mydb.commit()


        for id_almacen, costo in datos:
            plt.plot(x=id_almacen, y= costo)


    
#------------------------------FIN TABLA TICKET---------------------------------------


#-----------------------------------------TABLA DETALLE TICKET-------------------------------------------------
    def fn_registrardeti(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        mycursor = mydb.cursor()
        clavtide = self.clave_tic_deta.text()
        clavprde = self.clave_prod_deta.text()
        cantde = self.cant_deta.text()
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_8.setValue(int(x))
        sql = "INSERT INTO detalles_tickets (id_ticket, clave_producto, cantidad) VALUES(%s, %s, %s)"
        val = (clavtide, clavprde, cantde)
        mycursor.execute(sql, val)
        cantde = self.cant_deta.text()
        clavprde = self.clave_prod_deta.text()
        mycursor.execute("""UPDATE almacenes_productos SET cantidad = cantidad - %s WHERE id_producto = %s""", (cantde, clavprde))

        self.clave_tic_deta.clear()
        self.clave_prod_deta.clear()
        self.cant_deta.clear()
        self.clave_tic_deta.setFocus()
        mydb.commit()

    
    def fn_refreshdeti(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="password",
        database="farmacia"
        )
        x = 0
        while x < 100:
            x += 0.0001
            self.progreso_8.setValue(int(x))
        mycursor = mydb.cursor()
        mycursor.execute("SELECT detalles_tickets.id_ticket, detalles_tickets.clave_producto, productos.descripcion, detalles_tickets.cantidad \
                            FROM detalles_tickets \
                            INNER JOIN productos \
                            ON detalles_tickets.clave_producto = productos.clave_producto;")
        datos = mycursor.fetchall()
        i = len(datos)
        self.tbl_deta.setRowCount(i)

        tablerow = 0
        for id_ticket, clave_producto, descripcion, cantidad in datos:
            self.tbl_deta.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(id_ticket)))
            self.tbl_deta.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(clave_producto)))
            self.tbl_deta.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(descripcion))
            self.tbl_deta.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(cantidad)))
            tablerow +=1
        mydb.commit()
        self.clave_tic_deta.clear()
        self.clave_prod_deta.clear()
        self.cant_deta.clear()
        self.clave_tic_deta.setFocus()

#------------------------------FIN TABLA DETALLE_TICKET---------------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = farmacia_DB()
    GUI.show()
    sys.exit(app.exec_())