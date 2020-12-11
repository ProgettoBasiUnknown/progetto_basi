from flask import *
from flask_login import *
from sqlalchemy import *
app= Flask(__name__)
app.config[ 'SECRET_KEY'] = 'shish'
login_manager = LoginManager()
login_manager.init_app(app)

def is_admin(user):
	if user.gestore :
		return True
	else:
		return False
def is_client(user):
	if user.gestore :
		return False
	else:
		return True             

class User( UserMixin ):
# costruttore di classe
	def __init__( self , data ):
		self.id = data[0]
		self.nome = data[1]
		self.cognome = data[2]
		self.email = data[3]
		self.pwd = data[4]
		self.Telefono = data[5]
		self.gestore = data[6]

@login_manager.user_loader
def load_user(user_id):
		utente=richiesta_utente(user_id)
		risposta = User(utente)
	return risposta#######################

@app.route('/') ##home, la pagina html riceverà una lista delle proiezioni in ordine cronologico, spetta a noi decidere
def home():		##quante proiezioni mostrare, magari troncando la lista qui o non leggendola tutta nel documento html
	if is_authenticated() and is_admin(load_user(get_id())):	
		return redirect("/gestore")
	else: 
		return render_template("home.html")##fatta già una bozza

@app.route('/programmazione') ##mostra tutte le proiezioni 
def programmazione():

@app.route('/accedi')	##pagina per fare il login
def access()
	return render_template("accesso.html") ##fatta(scarnissima)

@app.route ("/login", methods =[ "POST"]) ##riceve i dati da /accedi e verifica,
def logger():				
	mail=request.form['email']
	pwd=request.form['password']
	id_ricevuto = verifica_credenziali(mail,pwd) ##verifica_credenziali torna -2 se non esiste la mail nel db e -1 se la pwd è errata, restituirà un html col risultato dell'operazione
	if( id_ricevuto >= 0):
		login_user(load_user(id_ricevuto))
		return render_template("risulato.html", result=True , link="/personale")			##se i dati sono giusti va nell'area riservata
			
	return return render_template("risulato.html", result=False , link="/login")		##se o dati sono errati torna alla home

@app.route('/registrati')	##campi dati da riempire per registrarsi
def register()
	return render_template("registrazione.html")

@app.route('/registrazione', methods =[ "POST"]) ##riceve i dati da /registrati , e li passa ad una funzione che controlla ed eventuamente registra nel db, restituirà un html col risultato dell'operazione
def registerer()
	n=request.form['nome']
	c=request.form['cognome']
	m=request.form['email']
	p=request.form['password']
	t=request.form['telefono']
	if(-----):
		risultato = inserimento_utente(n,c,m,p,t)
	
@app.route('/gestione')##home del gestore, dove può scegliere se gestire film/proiezioni, promuovere/declassare utenti/gestori (se è un gestore proprietario) e controllare le statistiche
@login_required
def gestore():
	if is_admin(load_user(get_id())) :
		return render_template('gestione.html')
	else:
		return redirect('/accedi')
			#accesso negato	
			
@app.route('/gestisci_film') ##qui verranno mostrati i film attualmente presenti nel db e i form per rimuoverli o aggiungerli
@login_required
def film_managing():
	if is_admin(load_user(get_id())) :
		return 
	else:
		return redirect('/accedi')
			#accesso negato	

@app.route('/aggiungi_film') ##riceverà le informazioni sul film da aggiungere e le trasmetterà al db, restituirà un html col risultato dell'operazione
@login_required
def add_film():
	if is_admin(load_user(get_id())) :
		return 
	else:
		return redirect('/accedi')
			#accesso negato	

@app.route('/rimuovi_film') ##riceverà le informazioni sul film da rimuovere e le trasmetterà al db, restituirà un html col risultato dell'operazione
@login_required	
def remove_film():
	if is_admin(load_user(get_id())) :
		return 
	else:
		return redirect('/accedi')
			#accesso negato	
	

@app.route('/autorizzazioni') ##mostra la lista utenti e i form per promuovere o declassare
@login_required
def authorizations():
	utente=load_user(get_id())
	if (is_admin(utente) and (utente.id== 0 or utente.id== 1 or utente.id== 2) ):
		return 
	else:
		return redirect('/accedi')
			#accesso negato	

@app.route('/promuovi')  ##elabora la promozione di un utente con i dati ricevuti da /autorizzazioni, restituirà un html col risultato dell'operazione
@login_required
def promote():
	utente=load_user(get_id())
	if (is_admin(utente) and (utente.id== 0 or utente.id== 1 or utente.id== 2) ):
		return 
	else:
		return redirect('/accedi')
			#accesso negato	
		
@app.route('/declassa')  ##elabora il declassamento di un utente con i dati ricevuti da /autorizzazioni, restituirà un html col risultato dell'operazione
@login_required
def downgrade():
	utente=load_user(get_id())
	if (is_admin(utente) and (utente.id== 0 or utente.id== 1 or utente.id== 2) ):
		return 
	else:
		return redirect('/accedi')
			#accesso negato	
		
@app.route('/gestisci_proiezioni') ##mostra le proiezioni ancora disponibili dando la possibilità di aggiungerne o chiuderne
@login_required
def manage_projection():
	if is_admin(load_user(get_id())) :
		return 
	else:
		return redirect('/accedi')
			#accesso negato		
		
@app.route('/aggiungi_proiezione') ##elabora la richiesta di aggiungere una nuova proiezione da /gestisci_proiezioni , restituirà un html col risultato dell'operazione
@login_required
def add_projection():
	if is_admin(load_user(get_id())) :
		return 
	else:
		return redirect('/accedi')
			#accesso negato	

@app.route('/chiudi_proiezione') ##elabora la richiesta di chiudere le prenotazioni per una proiezione proveniente da /gestisci_proiezioni , restituirà un html col risultato dell'operazione
@login_required
def close_projection():
	if is_admin(load_user(get_id())) :
		return 
	else:
		return redirect('/accedi')
			#accesso negato	

@app.route('/statistiche') ## mostra varie statistiche
@login_required
def stats():
	if is_admin(load_user(get_id())) :
		return 
	else:
		return redirect('/accedi')
			#accesso negato	



@app.route('/personale') ## pagina personale dell'utente dalla quale può controllare i suoi dati, le prenotazioni e fare nuovi prenotazioni
@login_required
def personal():
	return render_template("area_personale.html", utente=load_user(get_id()))

@app.route('/prenotazioni') ##mostra la lista delle prenotazioni effettuate
@login_required
def bookings():
	return render_template("prenotazioni.html", prenotazioni=prenotazioni_utente(get_id()))

@app.route('/prenotabili') ##mostra tutte le proiezioni prenotabili e dà un form per effettuare una prenotazione
def programmazione():

@app.route('/prenota', proiezione_id) ##elabora la prenotazione, restituirà un html col risultato dell'operazione
@login_required
def prenota():
	

