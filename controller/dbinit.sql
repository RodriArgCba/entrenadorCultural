CREATE TABLE IF NOT EXISTS Usuarios (
	NroDeEmpleado INTEGER PRIMARY KEY,
   	Nombre TEXT NOT NULL,
	Email TEXT NOT NULL,
	Administrador BOOLEAN NOT NULL
) ;

CREATE TABLE IF NOT EXISTS CulturasObjetivo (
	CulturaObjetivoId INTEGER PRIMARY KEY,
   	Nombre TEXT NOT NULL,
	Descripcion TEXT NOT NULL
) ;

CREATE TABLE IF NOT EXISTS Conversaciones (
	ConversacionId INTEGER PRIMARY KEY,
   	Nombre TEXT NOT NULL,
	Descripcion TEXT NOT NULL,
	Duracion NUMERIC(100,40) NOT NULL,
	CulturaObjetivoId INTEGER NOT NULL,
	UbicacionMP3 TEXT NOT NULL,
	FOREIGN KEY (CulturaObjetivoId) 
      REFERENCES CulturasObjetivo (CulturaObjetivoId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
) ;

CREATE TABLE IF NOT EXISTS Simulaciones (
	SimulacionId INTEGER PRIMARY KEY,
   	Fecha DATE NOT NULL,
	ConversacionId INTEGER NOT NULL,
	UsuarioId INTEGER NOT NULL,
	CalificacionDeUsuario INTEGER NOT NULL,
	FOREIGN KEY (ConversacionId) 
      REFERENCES Conversaciones (ConversacionId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION,
	FOREIGN KEY (UsuarioId) 
      REFERENCES Usuarios (UsuarioId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
) ;

CREATE TABLE IF NOT EXISTS Capturas (
	CapturaId INTEGER PRIMARY KEY,
	VolumenDeVoz NUMERIC(100,40) NOT NULL,
	PalabrasPorSegundo NUMERIC(100,40) NOT NULL,
	Posicion Brazos INTEGER NOT NULL,
	Mirada INTEGER NOT NULL,
	Rostro INTEGER NOT NULL,
	Cabeza INTEGER NOT NULL
) ;

CREATE TABLE IF NOT EXISTS Fases (
	FaseId INTEGER PRIMARY KEY,
   	Nombre TEXT NOT NULL,
	Tema TEXT NOT NULL,
	TiempoInicio NUMERIC(100,40) NOT NULL,
	Duracion NUMERIC(100,40) NOT NULL,
	Texto TEXT NOT NULL,
	CapturaEsperadaId INTEGER NOT NULL,
	ConversacionId INTEGER NOT NULL,
	FOREIGN KEY (CapturaEsperadaId) 
      REFERENCES Capturas (CapturaId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION,
	FOREIGN KEY (ConversacionId) 
      REFERENCES Conversaciones (ConversacionId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
) ;

CREATE TABLE IF NOT EXISTS Interpretaciones (
	InterpretacionId INTEGER PRIMARY KEY,
   	Lectura TEXT NOT NULL,
	MasInfo TEXT NOT NULL,
	CapturaId INTEGER NOT NULL,
	CulturaObjetivoId INTEGER NOT NULL,
	FOREIGN KEY (CapturaId) 
      REFERENCES Capturas (CapturaId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION,
	FOREIGN KEY (CulturaObjetivoId) 
      REFERENCES CulturasObjetivo (CulturaObjetivoId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
) ;

CREATE TABLE IF NOT EXISTS LineasDeResultado (
	LineaDeResultadoId INTEGER PRIMARY KEY,
	FaseId INTEGER NOT NULL,
	CapturaId INTEGER NOT NULL,
	InterpretacionId INTEGER NOT NULL,
	SimulacionId INTEGER NOT NULL,
 	FOREIGN KEY (FaseId) 
      REFERENCES Fases (FaseId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION,
	FOREIGN KEY (InterpretacionId) 
      REFERENCES Interpretaciones (InterpretacionId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION,
	FOREIGN KEY (SimulacionId) 
      REFERENCES Simulaciones (SimulacionId) 
         ON DELETE NO ACTION
         ON UPDATE NO ACTION
) ;




INSERT INTO Usuarios VALUES(1,"Rodrigo Banno","rodribanno@gmail.com",0);

INSERT INTO CulturasObjetivo VALUES(1,"Japonesa","En Japón, las interrelaciones personales están muy influenciadas por las ideas de «deber», «honor» y «obligación», conjunto conocido como giri (義理?), y que representa una costumbre diferente a la cultura individualista de las naciones occidentales. Las concepciones de «conductas deseables» y «moralidad» son menos practicadas en situaciones familiares, escolares y de amistad; sin embargo, se observa una práctica más formal frente a superiores o gente desconocida.");
INSERT INTO CulturasObjetivo VALUES(2,"Finlandesa","La cultura de Finlandia combina el legado indígena, representado por el idioma nacional, el finés con sus raíces fino-úgricas y el sauna, combinado con la cultura nórdica y europea. Debido a su historia y localización geográfica, Finlandia ha sido influenciada por pueblos bálticos y germánicos, así como por los pasados poderes dominantes Suecia y Rusia. Hoy, es visible la influencia cultural estadounidense y el país ha aumentado los contactos con culturas distantes de Asia y África.");

INSERT INTO Conversaciones VALUES(1,"Saludo y presentaciones","¿Cuáles son las primeras impresiones que das al saludar?",180.2,1,"assets/JAPONSaludosYPresentaciones.mp3");
INSERT INTO Conversaciones VALUES(2,"Explicando el producto","¿Cuáles son las primeras impresiones que das al saludar?",180.2,1,"assets/JAPONSaludosYPresentaciones.mp3");
INSERT INTO Conversaciones VALUES(3,"Calmando al cliente","¿Cuáles son las primeras impresiones que das al saludar?",180.2,1,"assets/JAPONSaludosYPresentaciones.mp3");
INSERT INTO Conversaciones VALUES(4,"Saludo y presentaciones","¿Cuáles son las primeras impresiones que das al saludar?",180.2,2,"assets/JAPONSaludosYPresentaciones.mp3");

INSERT INTO Capturas VALUES(1,40.0,0.27,4,2,1,0);
INSERT INTO Capturas VALUES(2,40.0,0.27,4,1,4,0);
INSERT INTO "main"."Capturas"
("CapturaId", "VolumenDeVoz", "PalabrasPorSegundo", "Posicion", "Mirada", "Rostro", "Cabeza")
VALUES (3, 600, 0.50, 0, 0, 0, 0);

INSERT INTO Interpretaciones VALUES(1,"Considerado y dispuesto","lalalala",1,1);
INSERT INTO Interpretaciones VALUES(2,"Sumiso y servicial","lalalala",2,1);
INSERT INTO "main"."Interpretaciones"
("InterpretacionId", "Lectura", "MasInfo", "CapturaId", "CulturaObjetivoId")
VALUES (3, 'Explicación Genérica', 'Mas genérico imposible la verdad... no sabría que decirte', 3, 1);


INSERT INTO Fases VALUES(1,"Saludo","Primer contacto",0.0,1.0,"¡Buenas tardes! ¿Como se encuentra usted hoy?",1,1);
INSERT INTO Fases VALUES(2,"Preseentacion","Consideración y sumisión.",1.0,2.0,"Cuénteme un poco de usted por favor",2,1);

