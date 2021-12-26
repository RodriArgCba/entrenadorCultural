BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Usuarios" (
	"NroDeEmpleado"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"Administrador"	BOOLEAN NOT NULL,
	PRIMARY KEY("NroDeEmpleado")
);
CREATE TABLE IF NOT EXISTS "CulturasObjetivo" (
	"CulturaObjetivoId"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Descripcion"	TEXT NOT NULL,
	PRIMARY KEY("CulturaObjetivoId")
);
CREATE TABLE IF NOT EXISTS "Conversaciones" (
	"ConversacionId"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Descripcion"	TEXT NOT NULL,
	"Duracion"	NUMERIC(100, 40) NOT NULL,
	"CulturaObjetivoId"	INTEGER NOT NULL,
	"UbicacionMP3"	TEXT NOT NULL,
	FOREIGN KEY("CulturaObjetivoId") REFERENCES "CulturasObjetivo"("CulturaObjetivoId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	PRIMARY KEY("ConversacionId")
);
CREATE TABLE IF NOT EXISTS "Simulaciones" (
	"SimulacionId"	INTEGER,
	"Fecha"	TIMESTAMP NOT NULL,
	"ConversacionId"	INTEGER NOT NULL,
	"UsuarioId"	INTEGER NOT NULL,
	"CalificacionDeUsuario"	INTEGER NOT NULL,
	FOREIGN KEY("ConversacionId") REFERENCES "Conversaciones"("ConversacionId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	FOREIGN KEY("UsuarioId") REFERENCES "Usuarios"("UsuarioId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	PRIMARY KEY("SimulacionId")
);
CREATE TABLE IF NOT EXISTS "Capturas" (
	"CapturaId"	INTEGER,
	"VolumenDeVoz"	NUMERIC(100, 40) NOT NULL,
	"PalabrasPorSegundo"	NUMERIC(100, 40) NOT NULL,
	"Posicion"	Brazos INTEGER NOT NULL,
	"Mirada"	INTEGER NOT NULL,
	"Rostro"	INTEGER NOT NULL,
	"Cabeza"	INTEGER NOT NULL,
	PRIMARY KEY("CapturaId")
);
CREATE TABLE IF NOT EXISTS "Fases" (
	"FaseId"	INTEGER,
	"Nombre"	TEXT NOT NULL,
	"Tema"	TEXT NOT NULL,
	"TiempoInicio"	NUMERIC(100, 40) NOT NULL,
	"Duracion"	NUMERIC(100, 40) NOT NULL,
	"Texto"	TEXT NOT NULL,
	"CapturaEsperadaId"	INTEGER NOT NULL,
	"ConversacionId"	INTEGER NOT NULL,
	FOREIGN KEY("CapturaEsperadaId") REFERENCES "Capturas"("CapturaId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	FOREIGN KEY("ConversacionId") REFERENCES "Conversaciones"("ConversacionId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	PRIMARY KEY("FaseId")
);
CREATE TABLE IF NOT EXISTS "Interpretaciones" (
	"InterpretacionId"	INTEGER,
	"Lectura"	TEXT NOT NULL,
	"MasInfo"	TEXT NOT NULL,
	"CapturaId"	INTEGER NOT NULL,
	"CulturaObjetivoId"	INTEGER NOT NULL,
	FOREIGN KEY("CapturaId") REFERENCES "Capturas"("CapturaId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	FOREIGN KEY("CulturaObjetivoId") REFERENCES "CulturasObjetivo"("CulturaObjetivoId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	PRIMARY KEY("InterpretacionId")
);
CREATE TABLE IF NOT EXISTS "LineasDeResultado" (
	"LineaDeResultadoId"	INTEGER,
	"FaseId"	INTEGER NOT NULL,
	"CapturaId"	INTEGER NOT NULL,
	"InterpretacionId"	INTEGER NOT NULL,
	"SimulacionId"	INTEGER NOT NULL,
	FOREIGN KEY("InterpretacionId") REFERENCES "Interpretaciones"("InterpretacionId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	FOREIGN KEY("FaseId") REFERENCES "Fases"("FaseId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	FOREIGN KEY("SimulacionId") REFERENCES "Simulaciones"("SimulacionId") ON DELETE NO ACTION ON UPDATE NO ACTION,
	PRIMARY KEY("LineaDeResultadoId")
);
INSERT INTO "Usuarios" VALUES (1,'Rodrigo Banno','rodribanno@gmail.com',0);
INSERT INTO "CulturasObjetivo" VALUES (0,'NO','NO');
INSERT INTO "CulturasObjetivo" VALUES (1,'Japonesa','En Japón, las interrelaciones personales están muy influenciadas por las ideas de «deber», «honor» y «obligación», conjunto conocido como giri (義理?), y que representa una costumbre diferente a la cultura individualista de las naciones occidentales. Las concepciones de «conductas deseables» y «moralidad» son menos practicadas en situaciones familiares, escolares y de amistad; sin embargo, se observa una práctica más formal frente a superiores o gente desconocida.');
INSERT INTO "CulturasObjetivo" VALUES (2,'Latinoamericana','La cultura latinoamericana e caracteriza por gente abierta y amigable, aunque a veces es considerada algo desorganizada y poco seria.');
INSERT INTO "Conversaciones" VALUES (1,'Prestando servicio técnico','Tienes que atender el reclamo o consulta de un cliente de Japón. ¿Cómo te desenvolverás?',500,1,'assets/JAPONServicioAlCliente.mp3');
INSERT INTO "Conversaciones" VALUES (2,'Prestando servicio al cliente','Tienes que atender el reclamo o consulta de un cliente latinoamericano. ¿Cómo te desenvolverás?',500,2,'assets/LATINOAMERICAServicioAlCliente.mp3');
INSERT INTO "Capturas" VALUES (0,0,0,0,0,0,0);
INSERT INTO "Capturas" VALUES (1,46,1.8,0,0,1,0);
INSERT INTO "Capturas" VALUES (2,20,1,0,0,4,0);
INSERT INTO "Capturas" VALUES (3,0,0,1,0,2,0);
INSERT INTO "Fases" VALUES (1,'Presentación','Saludo cordial y presentarse',0,50,'Buenos dias, gracias por atender mi reclamo.',2,1);
INSERT INTO "Fases" VALUES (2,'Respondiendo la consulta','Resolviendo problemas del cliente',50,350,'Ultimamente la maquinaria que adquirimos de su empresa ha estado dando muchos problemas. Los tractores se paran sin motivo 3 veces por dia, son muy ruidosos y están generando olor a quemado de manera constante... ¿Cuál puede ser el problema?',2,1);
INSERT INTO "Fases" VALUES (3,'Aliviando tensiones','Resolución de conflictos',400,100,'Mire... ya estamos bastante disconformes con los productos, y su servicio al cliente por teléfono deja mucho que desear. Pienso que vamos a tener que cesar de trabajar con su compañía.',2,1);
INSERT INTO "Fases" VALUES (4,'Presentación','Saludar y presentarse.',0,50,'¡Buenas! ¿Como anda todo?',1,2);
INSERT INTO "Fases" VALUES (5,'Respondiendo la consulta','Resolviendo problemas del cliente',50,350,'No es para ofender, pero los tractores están dando muchos problemas. Se paran sin motivo 3 veces por dia, hacen muchísimo ruido y huelen a quemado...',1,2);
INSERT INTO "Fases" VALUES (6,'Aliviando tensiones','Resolución de conflictos',400,100,'Te voy a ser sincero, no estamos conformes, como estan las cosas preferiríamos cesar el acuerdo que tenemos con ustedes como proveedores. No nos sirve y su servicio telefónico es de pésima calidad...',1,2);
INSERT INTO "Interpretaciones" VALUES (0,'No se pudo interpretar la captura','La cultura objetivo seleccionada no posee una interpretación para los datos capturados del usuario. Se enviará un reporte de este error al administrador de base de datos de forma automática, para que solicite la carga de una interpretación adecuada a la cultura. ¡Gracias por su paciencia!',0,0);
INSERT INTO "Interpretaciones" VALUES (1,'Arrogante, disarmonico, que no piensa en el grupo.','En japón, así como en muchos otros países orientales, la asertividad occidental suele verse como una actitud prepotente y arrogante. Se valora mucho mas una forma de ser armoniosa que no destaque demasiado y tenga en cuenta el ambiente y los sentimientos de todos. Se recomiendo intentar una voz mas neutral y no tan veloz. Recuerda que los japoneses son muy corteses, por lo que no te harán saberlo aunque estés actuando inapropiadamente, simplemente no te volverán a contactar en el futuro.',1,1);
INSERT INTO "Interpretaciones" VALUES (2,'Armonioso, considerado','Una actitud mas sumisa y servicial refleja los valores de la cultura japonesa. ¡Bien Hecho! Recuerda que los japoneses son muy corteses, por lo que no te harán saberlo aunque estés actuando inapropiadamente, simplemente no te volverán a contactar en el futuro.',2,1);
INSERT INTO "Interpretaciones" VALUES (3,'Conflictivo','Disonante y que va en contra de la corriente y de la armonía del grupo. La falta de sonrisa y disposición muestra una actitud inaceptable. Se recomiendo intentar sonreir y descruzar los brazos. Recuerda que los japoneses son muy corteses, por lo que no te harán saberlo aunque estés actuando inapropiadamente, simplemente no te volverán a contactar en el futuro.',3,1);
INSERT INTO "Interpretaciones" VALUES (4,'Asertivo, confiable','Los latinoamericano, así como muchos otros países occidentales, valoran mucho alguien confiado y que se hace escuchar. ¡Bien Hecho!',1,2);
INSERT INTO "Interpretaciones" VALUES (5,'Desconfiado, baja autoestima','En la cultura latinoamericana se valora que alguien esté confiado en sus conocimiento y capacidades y que demuestre esa confianza en su tono de voz y posición corporal. Se recomienda hablar mas fuerte y algo ams rápido (aunque no demasiado) y sonreir mas.',2,2);
INSERT INTO "Interpretaciones" VALUES (6,'Reflexivo, concentrado','Una actitud seria y que busca que las cosas sean justas se respeta en esta cultura. Sin embargo, las personas pueden sentirse intimidados por esta actitud y usted dará la impresión de ser inaccesible. Se recomienda descruzar los brazos y mostrar una actitud mas positiva con una sonrisa.',3,2);
COMMIT;