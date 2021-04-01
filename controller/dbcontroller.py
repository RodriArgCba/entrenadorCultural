# import pyodbc
import sqlite3

from model.captura import Captura
from model.conversacion import Conversacion
from model.culturaobjetivo import CulturaObjetivo
from model.direccionmirada import DireccionMirada
from model.fase import Fase
from model.interpretacion import Interpretacion
from model.movimientocabeza import MovimientoCabeza
from model.posicionbrazos import PosicionBrazos
from model.rostro import Rostro
from model.simulacion import Simulacion

con = sqlite3.connect('sqlitedb.db')
cursorObj = con.cursor()


def allculturas():
    cursorObj.execute("SELECT * FROM CulturasObjetivo")
    resultados = []
    for x in cursorObj.fetchall():
        cultura = CulturaObjetivo(x[1], x[2])
        cultura.id = x[0]
        cultura.interpretaciones = interpretacionesDeCultura(cultura)
        resultados.append(cultura)
    return resultados


def interpretacionesDeCultura(cultura: CulturaObjetivo):
    cursorObj.execute(f"SELECT * FROM Interpretaciones WHERE CulturaObjetivoId={cultura.id}")
    resultados = []
    for x in cursorObj.fetchall():
        interpretacion = Interpretacion(x[1], x[2], capturaporid(x[3]))
        interpretacion.id = x[0]
        resultados.append(interpretacion)
    return resultados


def conversacionesdecultura(cultura: CulturaObjetivo):
    print(f"SELECT * FROM Conversaciones WHERE CulturaObjetivoId={cultura.id}")
    cursorObj.execute(f"SELECT * FROM Conversaciones WHERE CulturaObjetivoId={cultura.id}")
    resultados = []
    for x in cursorObj.fetchall():
        conversacion = Conversacion(x[1], x[2], x[3], cultura, x[5])
        conversacion.id = x[0]
        conversacion.fases = fasesdeconversacion(conversacion)
        resultados.append(conversacion)
    return resultados


def capturaporid(capturaid):
    cursorObj.execute(f"SELECT * FROM Capturas WHERE CapturaId={capturaid}")
    x = cursorObj.fetchone()
    captura = Captura(float(x[1]), float(x[2]), PosicionBrazos(int(x[3])), DireccionMirada(int(x[4])),
                      Rostro(int(x[5])), MovimientoCabeza(int(x[6])))
    captura.id = x[0]
    return captura


def fasesdeconversacion(conversacion: Conversacion):
    print(f"SELECT * FROM Fases WHERE ConversacionId={conversacion.id}")
    cursorObj.execute(f"SELECT * FROM Fases WHERE ConversacionId={conversacion.id}")
    resultados = []
    for x in cursorObj.fetchall():
        fase = Fase(x[1], x[2], float(x[3]), float(x[4]), x[5], capturaporid(x[6]))
        fase.id = x[0]
        resultados.append(fase)
    return resultados


def guardarresultado(simulacion: Simulacion):
    cursorObj.execute("""INSERT INTO Simulaciones (Fecha, ConversacionId,
                         UsuarioId, CalificacionDeUsuario) VALUES(?, ?, ?, ?)""",
                      (simulacion.fecha, simulacion.conversacion.id, 1, 100)
                      )
    cursorObj.execute("SELECT last_insert_rowid()")
    idsimulacion = cursorObj.fetchone()[0]
    for linearesultado in simulacion.resultados:
        captura = linearesultado.captura
        cursorObj.execute("""INSERT INTO Capturas (VolumenDeVoz, PalabrasPorSegundo,
                            Posicion, Mirada, Rostro, Cabeza) VALUES(?, ?, ?, ?, ?, ?)""",
                          (captura.volumendevoz, captura.palabrasporsegundo, captura.posicionbrazos.value,
                           captura.mirada.value, captura.rostro.value, captura.cabeza.value)
                          )
        cursorObj.execute("SELECT last_insert_rowid()")
        idcaptura = cursorObj.fetchone()[0]
        cursorObj.execute("""INSERT INTO LineasDeResultado (FaseId, CapturaId,
                            InterpretacionId, SimulacionId) VALUES(?, ?, ?, ?)""",
                          (linearesultado.fase.id, idcaptura, linearesultado.interpretacion.id, idsimulacion))
    con.commit()

# cnxn = pyodbc.connect("Driver={SQL Server Native Client 18.0};"
#                      "Server=SQLEXPRESS;"
#                      "Database=entrenadorCultural;"
#                      "uid=sa;pwd=cultura")

# cursor = cnxn.cursor()
