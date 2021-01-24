import datetime
import sqlalchemy
import os.path
from sqlalchemy import *


#engine = create_engine('sqlite:///file.db', echo = True)
metadata = MetaData() #da finire bene quando si fanno i vari file-moduli
engine = create_engine( 'mysql+mysqldb://utente:database@localhost/cinema', echo=True )
#########################################################################################

utenti = Table('utenti', metadata,
	Column('ID', Integer, primary_key=True),
	Column('nome', String(30), nullable = False),
	Column('cognome', String(30), nullable = False),
	Column('email', String(30), nullable = False, unique = True),
	Column('password', String(30), nullable = False),
	Column('telefono', String(30), nullable = False),
	Column('gestore', Boolean))

posti = Table('posti', metadata,
	Column('ID', Integer, primary_key=True),
	Column('riga', Integer),
	Column('colonna', Integer),
	Column('sala', Integer, ForeignKey('sale.SALA')))

film = Table('film', metadata,
	Column('CODICE', Integer, primary_key=True),
	Column('titolo', String(30), nullable = False),
	Column('durata', Integer, nullable = False),
	Column('pubblicazione', Integer, nullable = False),
	Column('regista', String(30)),
	Column('genere', String(30)),
	Column('availability', Boolean))

prenotazioni = Table('prenotazioni', metadata,
	Column('NUMERO', Integer, primary_key=True),
	Column('posti_prenotati', String(30)), #ForeignKey('posti.ID') è una stringa di tutti gli ID dei posti prenotati, con parser. es: 20-21-21 sono 3 posti prenotati nella sala 4
	Column('proiezione', Integer, ForeignKey('proiezioni.ETICHETTA')),
	Column('cliente', Integer, ForeignKey('utenti.ID')))

proiezioni = Table('proiezioni', metadata,
	Column('ETICHETTA', Integer, primary_key=True),
	Column('dataora', DateTime),
	Column('sala', Integer, ForeignKey('sale.SALA')),
	Column('film', Integer, ForeignKey('film.CODICE')),
	Column('availability', Boolean),
	Column('prezzo', Integer, nullable = False),
	Column('vendite', Integer))

sale = Table('sale', metadata,
	Column('SALA', Integer, primary_key=True),
	Column('capienza', Integer, nullable = False))

metadata.create_all( engine )

#########################################################################################

#azione: semplice inserimento di alcuni dati di partenza nel DB
#richiede: nada
def start_db():
	conn = engine.connect()
	#inserimento 4 nuovi utenti iniziali, i primi 3 hanno sempre potere di assumere o licenziare utenti e non devono essere licenziati (sono i proprietari del cinema)
	insu = utenti.insert()
	conn.execute(insu,[
		{'nome': "Luca",    'cognome': "Simonaggio", 'email': "875936@stud.unive.it", 'password': "875936", 'telefono': "875936", 'gestore': True},
		{'nome': "Lorenzo", 'cognome': "Piva",       'email': "873775@stud.unive.it", 'password': "873775", 'telefono': "873775", 'gestore': True}, 
		{'nome': "Radu",    'cognome': "Novac",      'email': "857630@stud.unive.it", 'password': "857630", 'telefono': "857630", 'gestore': True},
		{'nome': "Antonio", 'cognome': "Ciccio",     'email': "857631@stud.unive.it", 'password': "857630", 'telefono': "857630", 'gestore': True},
		{'nome': "Mario",   'cognome': "Rossi",      'email': "mario@stud.it",  	  'password': "mario",  'telefono': "4316",   'gestore': False}

		]) 
	#inserimento 3 nuovi film
	insf = film.insert()
	conn.execute(insf,[
		{'titolo': "filmA", 'durata': 100, 'pubblicazione': 2002, 'regista': "registaA",'genere': "comico",    'availability': True},
		{'titolo': "filmB", 'durata': 120, 'pubblicazione': 2014, 'regista': "registaB",'genere': "romantico", 'availability': True},
		{'titolo': "filmC", 'durata': 105, 'pubblicazione': 1999, 'regista': "registaC",'genere': "avventura", 'availability': True},
		{'titolo': "filmD", 'durata': 90,  'pubblicazione': 1994, 'regista': "registaD",'genere': "azione",    'availability': True},
		{'titolo': "filmE", 'durata': 180, 'pubblicazione': 2006, 'regista': "registaE",'genere': "azione",    'availability': True},
		{'titolo': "filmF", 'durata': 130, 'pubblicazione': 2019, 'regista': "registaF",'genere': "avventura", 'availability': True}])	
	#inserimento 7 sale del cinema, questa quantità non muta
	inss = sale.insert()
	conn.execute(inss,[
		{'SALA': 1, 'capienza': 6},
		{'SALA': 2, 'capienza': 8},
		{'SALA': 3, 'capienza': 4},
		{'SALA': 4, 'capienza': 6},
		{'SALA': 5, 'capienza': 6},
		{'SALA': 6, 'capienza': 6},
		{'SALA': 7, 'capienza': 4}])
	#inserimento di quantità di posti a sedere diverso per ogni sala, questo numero rimarrà invariato, l'ID è incrementale-automatico
	inspo = posti.insert()
	conn.execute(inspo,[
		{'riga': 1, 'colonna': 1, 'sala': 1},#1
		{'riga': 1, 'colonna': 2, 'sala': 1},
		{'riga': 1, 'colonna': 3, 'sala': 1},
		{'riga': 2, 'colonna': 1, 'sala': 1},
		{'riga': 2, 'colonna': 2, 'sala': 1},
		{'riga': 2, 'colonna': 3, 'sala': 1},
		{'riga': 1, 'colonna': 1, 'sala': 2},#7
		{'riga': 1, 'colonna': 2, 'sala': 2},#8
		{'riga': 1, 'colonna': 3, 'sala': 2},
		{'riga': 1, 'colonna': 4, 'sala': 2},
		{'riga': 2, 'colonna': 1, 'sala': 2},
		{'riga': 2, 'colonna': 2, 'sala': 2},
		{'riga': 2, 'colonna': 3, 'sala': 2},
		{'riga': 2, 'colonna': 4, 'sala': 2},	#14	
		{'riga': 1, 'colonna': 1, 'sala': 3},	
		{'riga': 1, 'colonna': 2, 'sala': 3},	
		{'riga': 2, 'colonna': 1, 'sala': 3},	
		{'riga': 2, 'colonna': 2, 'sala': 3},	
		{'riga': 1, 'colonna': 1, 'sala': 4},	
		{'riga': 1, 'colonna': 2, 'sala': 4},	
		{'riga': 1, 'colonna': 3, 'sala': 4},	
		{'riga': 2, 'colonna': 1, 'sala': 4},	
		{'riga': 2, 'colonna': 2, 'sala': 4},	
		{'riga': 2, 'colonna': 3, 'sala': 4},			
		{'riga': 1, 'colonna': 1, 'sala': 5},	
		{'riga': 1, 'colonna': 2, 'sala': 5},	
		{'riga': 1, 'colonna': 3, 'sala': 5},	
		{'riga': 2, 'colonna': 1, 'sala': 5},	
		{'riga': 2, 'colonna': 2, 'sala': 5},	
		{'riga': 2, 'colonna': 3, 'sala': 5},	
		{'riga': 1, 'colonna': 1, 'sala': 6},
		{'riga': 1, 'colonna': 2, 'sala': 6},
		{'riga': 1, 'colonna': 3, 'sala': 6},
		{'riga': 2, 'colonna': 1, 'sala': 6},
		{'riga': 2, 'colonna': 2, 'sala': 6},
		{'riga': 2, 'colonna': 3, 'sala': 6},
		{'riga': 1, 'colonna': 1, 'sala': 7},
		{'riga': 1, 'colonna': 2, 'sala': 7},
		{'riga': 2, 'colonna': 1, 'sala': 7},
		{'riga': 2, 'colonna': 2, 'sala': 7}])
			
	inserimento_proiezione(datetime.datetime(2020,10,3),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,5,13),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,11,23),4,2,7)##
	inserimento_proiezione(datetime.datetime(2020,12,8),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,6,18),4,2,7)
	inserimento_proiezione(datetime.datetime(2020,12,14),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,2,6),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,2,7),4,2,7)
	inserimento_proiezione(datetime.datetime(2020,1,2),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,2,1),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,3,1),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,4,1),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,5,1),4,2,6)
	inserimento_proiezione(datetime.datetime(2020,6,1),4,2,6)
	inserimento_proiezione(datetime.datetime(2020, 7, 1), 2, 1, 8)
	inserimento_proiezione(datetime.datetime(2020, 8, 2), 4, 4, 10)#orario, salaID, filmID, prezzo
	inserimento_proiezione(datetime.datetime(2020, 9, 5), 1, 2, 9)

	inserisci_prenotazione("7-8-", 3, 4, 2)
	inserisci_prenotazione("9-", 3, 4, 1)
	inserisci_prenotazione("10-", 3, 4, 1)
	inserisci_prenotazione("11-12-13-", 3, 4, 3)
	inserisci_prenotazione("7-8-9-10-11", 4, 2, 5)#posti, proiezione, cliente, num_posti
	#inserimento di alcune proiezioni in programma che verranno aggiunte ed eleminate con le nuove pellicole appena uscite
	#inspr = proiezioni.insert()
	#conn.execute(inspr,[])
	#inspro = prenotazioni.insert()
	#conn.execute(inspro,[])
	conn.close()
	
#########################################################################################

#azione: inserimento di un nuovo film nel db
#richiede: titolo(str), durata(int), pubblicazione(int), regista(str), genere(str)
def inserimento_film(titolo, durata, pubblicazione, regista, genere):
	#richiesta connessione
	conn = engine.connect()
	#insert
	ins = film.insert()
	conn.execute(ins,
		[{'titolo': titolo, 'durata': durata, 'pubblicazione': pubblicazione, 'regista': regista, 'genere': genere, 'availability': True }])
	#chiusura connessione
	conn.close()

#########################################################################################

#azione: inserimento nuovo utente tramite i dati forniti nell'interfaccia web, ID sarò incrementale e gestore di deafault a false
#richiede: nome(str) cognome(str) email(str) pass(str) telefono(int)
def inserimento_utente(nome, cognome, mail, password, tel):
	conn=engine.connect()
	conn.execute(utenti.insert(),
		[{'nome':nome, 'cognome':cognome, 'email':mail, 'password': password, 'telefono': tel, 'gestore': False}])
	user = conn.execute(select([utenti]).where(utenti.c.email==mail)).first()
	conn.close()
	return user
	
#########################################################################################

#azione: inserimento nuova proiezione programmata da parte di un gestore
#richiede: orario del film (DateTime), Numero Sala(int), ID del film(int), prezzo(int)
def inserimento_proiezione(orario, salaID, filmID, prezzo):
	conn=engine.connect()
	conn.execute(proiezioni.insert(),
		[{'dataora':orario, 'sala':salaID, 'film':filmID, 'availability': True, 'prezzo': prezzo, 'vendite': 0}])
	conn.close()

#########################################################################################

#azione: film reso non più disponibile nella lista film ma non eliminato, operazione possibili da soli gestori
#richiede: ID(int)
def elimina_film(id): 
	conn=engine.connect()
	check = conn.execute(select([film]).where(film.c.CODICE ==id)).fetchone()
	if check != None:#controllo se il film è registrato
		tran = conn.begin()#inizio transazione
		try:
			conn.execute(film.update().values(availability = False).where(film.c.CODICE == id))
			tran.commit()
			conn.close()
			return True
		except:
			tran.rollback()
			conn.close()
			raise
		return False
	else:
		return False

#########################################################################################
#
#azione: eliminazione totale di una entry nella tabella utenti tramite ID, operazione fatta dall'utente stesso che vuole cancellare i propri dati del db
#richiede: ID(int)
#def elimina_utente(id):
#	conn=engine.connect()
#	conn.execute(utenti.delete().where(utenti.c.ID==id))
#	conn.close()
#
#########################################################################################

#azione: prelevare tutti i dati di un utente e ne restituisce un "dizionario"
#richiede: ID(int)
def richiesta_utente(id):
	conn = engine.connect()
	out = conn.execute(select([utenti]).where(utenti.c.ID == id)).first()
	conn.close()
	return out

#########################################################################################

#azione: promuove utente a gestore, operazione per soli admin
#richiede: ID(int)
def promuovi(id):
	if (id>3):
		conn = engine.connect()
		check =  conn.execute(select([utenti]).where(utenti.c.ID == id)).fetchone()
		if  check != None:#verifico l'esistenza dell'utente
			tran = conn.begin() ##inizio la transazione
			try:
				conn.execute(utenti.update().values(gestore = True).where(utenti.c.ID == id))
				tran.commit()
				conn.close()
				return True
			except:
				tran.rollback()
				conn.close()
				raise
			return False
		else:
			return False
#########################################################################################

#azione: declassa un gestore a semplice utente, operazione per soli admin, i numeri <4 saranno ignorati per sicurezza del db
#richiede: ID(int)
def licenzia(id):
	##aggiungere transazione
	
	if (id>3):
		conn = engine.connect()
		check =  conn.execute(select([utenti]).where(utenti.c.ID == id)).fetchone()
		if  check != None: #verifico l'esistenza dell'utente
			tran = conn.begin()#inizio transazione
			try:
				conn.execute(utenti.update().values(gestore = False).where(utenti.c.ID == id))
				tran.commit()
				conn.close()
				return True
			except:
				tran.rollback()
				conn.close()
				raise
			return False
		else:
			return False
#########################################################################################

#azione: aggiungere prenotazione
#richiede: posti prenotati(int), proiezione acquistata(int), cliente(int), numero posti prenotati(int)
def inserisci_prenotazione(posti, proiezione, cliente, num_posti):
	conn = engine.connect()
	conn.execute(prenotazioni.insert(),
		[{'posti_prenotati': posti, 'proiezione': proiezione, 'cliente': cliente}])
	vd = conn.execute(select([proiezioni.c.vendite]).where(proiezioni.c.ETICHETTA == proiezione)).fetchone()
	if vd != None:
		new_vendite = num_posti + vd[0]
		conn.execute(proiezioni.update().values(vendite = new_vendite).where(proiezioni.c.ETICHETTA == proiezione))
	conn.close()
	return True
#########################################################################################

#azione: restituire tutta la tabella utenti (tranne i primi 3) e serve per visualizzare chi poter promuovere o licenziare
#richiede: nada
def richiesta_tabella_utenti():
	conn = engine.connect()
	out = conn.execute(select([utenti]).where(utenti.c.ID > 3)).fetchall()
	conn.close()
	return out

#########################################################################################

#azione: restituire lista con tutte le proiezioni programmate, se condizione è false restituisce solo le proiezioni prenotabili
#richiede: condizione(boolean)
def richiesta_tabella_proiezioni(condizione):
	conn = engine.connect()
	if condizione:
		out = conn.execute(select([proiezioni, film]).where(proiezioni.c.film == film.c.CODICE).order_by('dataora')).fetchall()
	else:
		out = conn.execute(select([proiezioni, film]).where(and_(proiezioni.c.film == film.c.CODICE , proiezioni.c.availability == True)).order_by('dataora')).fetchall()		
	conn.close()
	return out

#########################################################################################

#azione: lista con dati utili riguardanti tutte le prenotazioni di un cliente
#richiede: ID(int)
def richiesta_prenotazioni_utente(id):
	conn = engine.connect()
	out = conn.execute(select([film.c.titolo,proiezioni.c.sala,proiezioni.c.dataora,prenotazioni.c.posti_prenotati]).where(and_(prenotazioni.c.cliente == id, proiezioni.c.film == film.c.CODICE, proiezioni.c.ETICHETTA==prenotazioni.c.proiezione)).order_by('dataora')).fetchall()
	conn.close()
	return out

#########################################################################################

#azione: restituisce tutti i film oppure solo quelli disponibili, dipende dal parametro passato
#richiede: condizione(bool)
def richiesta_tabella_film(cond):	
	conn = engine.connect()
	if(cond==True):
		out = conn.execute(select([film])).fetchall()
		conn.close()
		return out
	else:
		out = conn.execute(select([film]).where(film.c.availability==True)).fetchall()
		conn.close()
		return out

#########################################################################################
	
#azione: restituire tutte le sale disponibili
#richiede: nada
def richiesta_tabella_sale():
	conn = engine.connect()
	out = conn.execute(select([sale])).fetchall()
	conn.close()
	return out

#########################################################################################

#azione: verifico se una mail c'è già, se si ritorno true, in caso negativo false
#richiede:
def verifica_mail_db(mail):
	conn = engine.connect()
	out = conn.execute(select([utenti]).where(utenti.c.email == mail)).first()
	conn.close()
	if out==None:
		return False
	else:
		return True

#########################################################################################

#azione: verificare se mail e password di un utente corrispondono, ritorna -2 se non c'è la mail, -1 in caso di pasw sbagliata, ID dell'utente altrimenti
#richiede: una mail(str) e pass(str)
def verifica_credenziali(mail, password):
	conn = engine.connect()
	o = conn.execute(select([utenti]).where(utenti.c.email == mail))
	user = o.first()
	conn.close()
	if user==None:
		return -2
	else:
		if user['password']==password:
			return user['ID']
		else:
			return -1

#########################################################################################

#azione: cambia la disponibilità di una prenotazione in false, così da non essere più prenotabile
#richiede: k(int)
def disabilita_proiezione(k):
	conn=engine.connect()
	check =conn.execute(select([proiezioni]).where(proiezioni.c.ETICHETTA == k)).fetchone()
	if check != None:#controlla l'esistenza della proiezione
		tran = conn.begin()
		try:
			conn.execute(proiezioni.update().values(availability = False).where(proiezioni.c.ETICHETTA == k))#aggiorna la disponibilità
			tran.commit()
			conn.close()
			return True
		except:
			tran.rollback
			conn.close()
			raise
		return False	
	else:
		return False

#########################################################################################

#azione: restituisce un array con numero di vendite divise per mese e l'incasso annuale, serve per visualizzare le statistiche di vendita
#richiede: anno(int)
def statistiche_vendite_annuali(anno):
	conn = engine.connect()
	GEN = int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,1,1), proiezioni.c.dataora < datetime.datetime(anno,2,1)))).fetchone()[0])
	FEB = int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,2,1), proiezioni.c.dataora < datetime.datetime(anno,3,1)))).fetchone()[0])
	MAR = int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,3,1), proiezioni.c.dataora < datetime.datetime(anno,4,1)))).fetchone()[0])
	APR	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,4,1), proiezioni.c.dataora < datetime.datetime(anno,5,1)))).fetchone()[0])
	MAG	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,5,1), proiezioni.c.dataora < datetime.datetime(anno,6,1)))).fetchone()[0])
	GIU	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,6,1), proiezioni.c.dataora < datetime.datetime(anno,7,1)))).fetchone()[0])
	LUG	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,7,1), proiezioni.c.dataora < datetime.datetime(anno,8,1)))).fetchone()[0])
	AGO	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,8,1), proiezioni.c.dataora < datetime.datetime(anno,9,1)))).fetchone()[0])
	SET	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,9,1), proiezioni.c.dataora < datetime.datetime(anno,10,1)))).fetchone()[0])
	OTT	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,10,1), proiezioni.c.dataora < datetime.datetime(anno,11,1)))).fetchone()[0])
	NOV	= int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,11,1), proiezioni.c.dataora < datetime.datetime(anno,12,1)))).fetchone()[0])
	DIC = int(conn.execute(select([func.sum(proiezioni.c.vendite)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,12,1), proiezioni.c.dataora < datetime.datetime(anno+1,1,1)))).fetchone()[0])
	avg_price = conn.execute(select([func.avg(proiezioni.c.prezzo)]).where(and_(proiezioni.c.dataora >= datetime.datetime(anno,1,1), proiezioni.c.dataora < datetime.datetime(anno+1,1,1)))).fetchone()[0]
	incasso = (GEN+FEB+MAR+APR+MAG+GIU+LUG+AGO+SET+OTT+NOV+DIC) * avg_price
	#mettere tutttappostooo
	conn.close()
	return [[GEN,FEB,MAR,APR,MAG,GIU,LUG,AGO,SET,OTT,NOV,DIC], incasso]

#########################################################################################

#azione: restiuisce gli anni disponibili per visualizzare le statistiche
#richiede: nada
def anni_statistiche():
	conn = engine.connect()
	out = conn.execute(select([proiezioni.c.dataora]).distinct()).fetchall()
	years=[]
	for a in out[0]:
		years.append(a.year)
	o = list(set(years))
	return o

#########################################################################################

#azione: restiuisce i posti prenotatisotto forma di vettore di int ordinato (crescente)
#richiede: etichetta della proiezione(int)
def array_posti_prenotati(etichetta):
	conn = engine.connect()
	posti_occupati = conn.execute(select([prenotazioni.c.posti_prenotati]).where(prenotazioni.c.proiezione==etichetta)).fetchall()
	posti=""
	for a in posti_occupati:
		posti = posti+a[0]
	conn.close()
	lista = posti.split("-")
	del lista[-1]
	out=[]
	if not lista:
		return out
	for a in lista:
		out.append(int(a))
	return out #posti non dispobili

#########################################################################################

#azione: retituisce i posti di una SALA sotto forma di vettore di int ordinato
#richiede: etichetta della proiezione(int)
def array_posti_sala(etichetta):
	conn = engine.connect()
	#trovo l'id della sala tramite l'etichetta della proiezione
	salaN = conn.execute(select([proiezioni.c.sala]).where(proiezioni.c.ETICHETTA==etichetta)).fetchone()[0]
	posti_proiezione = conn.execute(select([posti]).where(posti.c.sala==salaN)).fetchall()
	#adesso devo ritornare la lista di tutti i posti della sala dopo la query
	#tutti_posti = ""
	#for a in posti_proiezione:
	#	tutti_posti=tutti_posti+a[0]+"-"
	#out = tutti_posti.split("-").sort()
	out=[]
	for posto in posti_proiezione:
		out.append(posto)
	conn.close()
	return out

#########################################################################################

#azione: restituisce i generi dei film presenti nelle proiezioni disponibili
#richiede:
def richiesta_generi_disponibili():
	conn = engine.connect()
	out=conn.execute(select([film.c.genere]).where(and_(film.c.CODICE==proiezioni.c.film, proiezioni.c.availability==True)).distinct()).fetchall()
	conn.close
	return out
	
#########################################################################################

#azione: restituisce le proiezioni disponibili con film di un determinati genere
#richiede: genere del film(boolean)
def richiesta_tabella_proiezioni_genere(genere):
	conn = engine.connect()
	out = conn.execute(select([proiezioni, film]).where(and_(proiezioni.c.film == film.c.CODICE , proiezioni.c.availability == True, film.c.genere==genere)).order_by('dataora')).fetchall()		
	conn.close()
	return out

#########################################################################################

#azione: controlla se una proiezione che un gestore vuole inserire non coincede utilizza sale già occupate
#richiede: ora della proiezione da inserire(datetime), sala da utilizzare(int), durata film in minuti(int)
def controlla_proiezione(ora, salaa, durata):
	conn = engine.connect()
	dopo = ora + datetime.timedelta(minutes = durata)
	out = conn.execute(select([proiezioni]).where(and_(proiezioni.c.dataora >= ora, proiezioni.c.dataora <= dopo, proiezioni.c.sala == salaa))).fetchone()
	if( out == None):
		return False
	else:
		return True	
	
#########################################################################################

#azione: ritorna la durata in minuti di un film
#richiede: id del film(int)
def durata_film(id):
	conn = engine.connect()
	out = conn.execute(select([film.c.durata]).where(film.c.CODICE == id)).fetchone()[0]
	conn.close()
	return out

#########################################################################################

#azione: verifica la presenza del film avente id='id' nel database
#richiede: id film (int)
def verifica_id_film(id):
	conn = engine.connect()
	out = conn.execute(select([film]).where(film.c.CODICE==id)).fetchone()
	if out==None:
		return True
	return False
	
#########################################################################################




#start_db()

