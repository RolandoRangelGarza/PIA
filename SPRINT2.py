import mysql.connector
import sys
from PyQt5 import QtWidgets
import pandas as pd
import matplotlib.pyplot as plt

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