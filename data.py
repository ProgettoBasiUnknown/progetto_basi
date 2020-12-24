import datetime
import sqlalchemy
from sqlalchemy import *


engine = create_engine('sqlite:///file.db', echo = True)
metadata = MetaData() #da finire bene quando si fanno i vari file-moduli

#########################################################################################

utenti = Table('utenti', metadata,
	Column('ID', Integer, primary_key=True),
	Column('nome', String),
	Column('cognome', String),
	Column('email', String),
	Column('password', String),
	Column('telefono', Integer),
	Column('gestore', Boolean))

prenotazioni = Table('prenotazioni', metadata,
	Column('NUMERO', Integer, primary_key=True),
	Column('posti_prenotati', String), #ForeignKey('posti.ID') è una stringa di tutti gli ID dei posti prenotati, con parser. es: 20-21-21 sono 3 posti prenotati nella sala 4
	Column('proiezione', Integer, ForeignKey('proiezioni.ETICHETTA')),
	Column('cliente', Integer, ForeignKey('utenti.ID')))

posti = Table('posti', metadata,
	Column('ID', Integer, primary_key=True),
	Column('riga', Integer),
	Column('colonna', Integer),
	Column('sala', Integer, ForeignKey('sale.SALA')))

film = Table('film', metadata,
	Column('CODICE', Integer, primary_key=True),
	Column('titolo', String),
	Column('durata', Integer),
	Column('pubblicazione', Integer),
	Column('regista', String),
	Column('genere', String),
	Column('availability', Boolean))

proiezioni = Table('proiezioni', metadata,
	Column('ETICHETTA', Integer, primary_key=True),
	Column('dataora', DateTime),
	Column('sala', Integer, ForeignKey('sale.SALA')),
	Column('film', Integer, ForeignKey('film.CODICE')),
	Column('availability', Boolean),
	Column('prezzo', Integer),
	Column('vendite', Integer))

sale = Table('sale', metadata,
	Column('SALA', Integer, primary_key=True),
	Column('capienza', Integer))

metadata.create_all( engine )

#########################################################################################

#azione: semplice inserimento di alcuni dati di partenza nel DB
#richiede: nada
def start_db():
	conn = engine.connect()
	#inserimento 4 nuovi utenti iniziali, gli ID 1-2-3 hanno sempre potere di assumere o licenziare utenti e non devono essere licenziati
	insu = utenti.insert()
	conn.execute(insu,[
		{'nome': "Luca",    'cognome': "Simonaggio", 'email': "875936@stud.unive.it", 'password': "875936", 'telefono': 875936, 'gestore': True},
		{'nome': "Lorenzo", 'cognome': "Piva",       'email': "873775@stud.unive.it", 'password': "873775", 'telefono': 873775, 'gestore': True}, 
		{'nome': "Radu",    'cognome': "Novac",      'email': "857630@stud.unive.it", 'password': "857630", 'telefono': 857630, 'gestore': True}, 
		{'nome': "Mario",   'cognome': "Rossi",      'email': "mario@stud.it",  	  'password': "mario",  'telefono': 4316,   'gestore': False}

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
		{'riga': 1, 'colonna': 1, 'sala': 1},
		{'riga': 1, 'colonna': 2, 'sala': 1},
		{'riga': 1, 'colonna': 3, 'sala': 1},
		{'riga': 2, 'colonna': 1, 'sala': 1},
		{'riga': 2, 'colonna': 2, 'sala': 1},
		{'riga': 2, 'colonna': 3, 'sala': 1},
		{'riga': 1, 'colonna': 1, 'sala': 2},
		{'riga': 1, 'colonna': 2, 'sala': 2},
		{'riga': 1, 'colonna': 3, 'sala': 2},
		{'riga': 1, 'colonna': 4, 'sala': 2},
		{'riga': 2, 'colonna': 1, 'sala': 2},
		{'riga': 2, 'colonna': 2, 'sala': 2},
		{'riga': 2, 'colonna': 3, 'sala': 2},
		{'riga': 2, 'colonna': 4, 'sala': 2},		
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
	#inserimento di alcune proiezioni in programma che verranno aggiunte ed eleminate con le nuove pellicole appena uscite
	#inspr = proiezioni.insert()
	#conn.execute(inspr,[])
	#inspro = prenotazioni.insert()
	#conn.execute(inspro,[])
	conn.close()
	inserimento_proiezione(datetime.datetime(2018, 6, 1), 2, 1, 8)
	inserimento_proiezione(datetime.datetime(2020, 6, 2), 4, 4, 10)
	inserimento_proiezione(datetime.datetime(2019, 7, 5), 1, 2, 9)


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
	user = conn.execute(select([utenti]).where(utenti.c.mail==mail)).first()
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
	conn.execute(film.update().values(availability = False).where(film.c.CODICE == id))
	conn.close()

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
	conn = engine.connect()
	conn.execute(utenti.update().values(gestore = True).where(utenti.c.ID == id))
	conn.close()

#########################################################################################

#azione: declassa un gestore a semplice utente, operazione per soli admin, i numeri <4 saranno ignorati per sicurezza del db
#richiede: ID(int)
def licenzia(id):
	if (id>3):
		conn = engine.connect()
		conn.execute(utenti.update().values(gestore = False).where(utenti.c.ID == id))
		conn.close()

#########################################################################################

#azione: aggiungere prenotazione
#richiede: il posto prenotato(int), proiezione acquistata(int), cliente(int)
def inserisci_prenotazione(posto, proiezione, cliente):
	conn = engine.connect()
	conn.execute(prenotazioni.insert(),
		[{'posti_prenotati': posto, 'proiezione': proiezione, 'cliente': cliente}])
	conn.close()
	#eventuali controlli li metto dopo
#########################################################################################

#azione: restituire tutta la tabella utenti (tranne i primi 3) e serve per visualizzare chi poter promuovere o licenziare
#richiede: nada
def richiesta_tabella_utenti():
	conn = engine.connect()
	out = conn.execute(select([utenti]).where(utenti.c.ID > 3)).fetchall()
	conn.close()
	return out

#########################################################################################

#azione: restituire lista con tutte le proiezioni programmate
#richiede: nada
def richiesta_tabella_proiezioni():
	conn = engine.connect()
	out = conn.execute(select([proiezioni, film]).where(proiezioni.c.film == film.c.CODICE).order_by('dataora')).fetchall()
	conn.close()
	return out

#########################################################################################

#azione: lista con tutte le prenotazioni di un cliente
#richiede: ID(int)
def richiesta_prenotazioni_utente(id):
	conn = engine.connect()
	out = conn.execute(select([prenotazioni]).where(prenotazioni.c.cliente == id)).fetchall()
	conn.close()
	return out

#########################################################################################

#azione: restituisce tutti i film oppure solo quelli disponibili, dipende dal parametro passato
#richiede: condizione(str)
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

#azione:
#richiede:
def disabilita_proiezione(k):
	conn=engine.connect()
	conn.execute(proiezioni.update().values(availability = False).where(proiezioni.c.ETICHETTA == k))
	conn.close()

#########################################################################################

#azione:
#richiede:

#########################################################################################

def stampa():
	licenzia(2)
	o = richiesta_tabella_utenti();
	for a in o:
		print(a)

#	conn = engine.connect()
#	s = select([utenti.c.ID, utenti.c.gestore]) 
#	results =conn.execute(s)
#	row = results.fetchone()
#	while(row != None):
#		print(row)
#		row = results.fetchone()


#########################################################################################



start_db()
#
stampa()

