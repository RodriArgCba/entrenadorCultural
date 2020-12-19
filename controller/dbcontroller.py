#import pyodbc
import sqlite3

con = sqlite3.connect('sqlitedb.db')
cursorObj = con.cursor()

#cnxn = pyodbc.connect("Driver={SQL Server Native Client 18.0};"
#                      "Server=SQLEXPRESS;"
#                      "Database=entrenadorCultural;"
#                      "uid=sa;pwd=cultura")

#cursor = cnxn.cursor()
