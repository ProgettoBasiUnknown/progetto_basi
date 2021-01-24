from flask import *
from flask_login import *
from sqlalchemy import *
from data import *

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
		utente=richiesta_utente(user_id)#query al database
		risposta = User(utente)#istanzio un oggetto di tipo utente
		return risposta

from functools import wraps	
	
def gestore_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		us=load_user(current_user.get_id())
		if us.gestore:
			return f(*args, **kwargs)
		else:
			return render_template("risultato.html", result=False , link="/", msg= "Pagina riservata ai gestori" )
	return wrap

def admin_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		us=load_user(current_user.get_id())
		if int(us.id)<=3:
			return f(*args, **kwargs)
		else:
			return render_template("risultato.html", result=False , link="/", msg= "Pagina riservata agli amministratori." )
	return wrap

####################################################

@app.route('/') #home, la pagina html riceverà una lista delle proiezioni in ordine cronologico, le opzioni per loggarsi, registrarsi, consultare programmazione e dati personali
def home():		
	proiezioni_vicine=richiesta_tabella_proiezioni(True)[:4]
	if current_user.is_authenticated :#controlla se si è già loggati
		u=load_user(current_user.get_id())
		if is_admin(u):
			return render_template("home.html", proiezioni = proiezioni_vicine, utente = u , gestore = True)
		else: 
			return render_template("home.html", proiezioni = proiezioni_vicine, utente = u)#altrimenti se si è un utente normale, si apre la pagina principale, mostrando un messaggio di benvenuto personalizzato e le opzioni per gli utenti registrati
	else: 
		return render_template("home.html", proiezioni = proiezioni_vicine)#se si accede senza essere loggati, si può solo accedere/registrare o controllare la programmazione
		
@app.route('/programmazione') #mostra tutte le proiezioni in programma
def programmazione():
		return render_template("programmazione.html", proiezioni = richiesta_tabella_proiezioni(True))

@app.route('/accedi')	##pagina per fare il login
def access():
	if current_user.is_authenticated:
		return render_template("personale.html", profilo=load_user(current_user.get_id()))
	else:
		return render_template("accesso.html") ##fatta(scarnissima)

@app.route ("/login", methods =[ "POST"]) ##riceve i dati da /accedi e verifica,
def logger():				
	mail=request.form['email']
	pwd=request.form['password']
	id_ricevuto = verifica_credenziali(mail,pwd) ##verifica_credenziali torna -2 se non esiste la mail nel db e -1 se la pwd è errata, restituirà un html col risultato dell'operazione
	if( id_ricevuto >= 0):
		login_user(load_user(id_ricevuto))
		if is_admin(load_user(current_user.get_id())) :
			return render_template("risultato.html", result=True , link="/gestione")		#se si accede come gestore si viene reindirizzati alla paginna di gestione
		return render_template("risultato.html", result=True , link="/personale")			#se i dati sono giusti va nell'area riservata
	else:		
		return render_template("risultato.html", result=False , link="/accedi")		#se o dati sono errati torna alla home

@app.route('/registrati')	# mostra i campi dati da riempire per registrarsi
def register():
	if current_user.is_authenticated: # se l'utente ha già eseguito l'accesso, viene reindirizzato alla pagina personale
		return render_template("area_personale.html", utente=load_user(current_user.get_id()))
	else:
		return render_template("registrazione.html")

@app.route('/registrazione', methods =[ "POST"]) ##riceve i dati da /registrati , e li passa ad una funzione che controlla ed eventuamente registra nel db, restituirà un html col risultato dell'operazione
def registerer():
	n=request.form['nome']
	c=request.form['cognome']
	m=request.form['email']
	p=request.form['password']
	t=request.form['telefono']
	if n=="" or c=="" or m=="" or p=="" or t=="" :
		return render_template("risultato.html", result=False , link="/registrati", msg="Dati inseriti insufficienti")
	if not(verifica_mail_db(m)): #verificà unicità della mail
		risultato = User(inserimento_utente(n,c,m,p,t)) #registrazione utente
		login_user(risultato) #login utente
		return render_template("risultato.html", result=True , link="/personale")
	else:
		return render_template("risultato.html", result=False , link="/registrati", msg="Email già registrata")
	

@app.route('/logout')
def logout():
	logout_user() #logout
	return render_template("risultato.html", result=True , link="/") #reindirizzamento alla pgina home
	
@app.route('/gestione')##home del gestore, dove può scegliere se gestire film/proiezioni, promuovere/declassare utenti/gestori (se è un gestore proprietario) e controllare le statistiche
@login_required
@gestore_required
def gestore():
	if int(current_user.get_id()) <= 3:
		return render_template('gestione.html', admin = True)##ANCORA DA SISTEMARE!!!!!!!!!!!
	else: 
		return render_template('gestione.html')
	
			
@app.route('/gestisci_film') ##qui verranno mostrati i film attualmente presenti nel db e i form per rimuoverli o aggiungerli
@login_required
@gestore_required
def film_managing():
	return render_template('gestione_films.html', films = richiesta_tabella_film(True))##ANCORA DA SISTEMARE!!!!!!!!!!!
	

@app.route('/aggiungi_film', methods =[ "POST"]) ##riceverà le informazioni sul film da aggiungere e le trasmetterà al db, restituirà un html col risultato dell'operazione
@login_required
@gestore_required
def add_film():
	titolo = request.form['titolo']
	durata = request.form['durata']
	pubblicazione = request.form['pubblicazione']
	regista = request.form['regista']
	genere = request.form['genere']
	inserimento_film(titolo,durata,pubblicazione,regista,genere)
	return render_template('risultato.html' , result = True, link = '/gestisci_film')
	

@app.route('/rimuovi_film', methods =[ "POST"]) ##riceverà le informazioni sul film da rimuovere e le trasmetterà al db, restituirà un html col risultato dell'operazione
@login_required
@gestore_required
def remove_film():
	id = request.form['id']
	resultq = elimina_film(id)
	return  render_template('risultato.html' , result = resultq, link = '/gestisci_film')
	
	

@app.route('/autorizzazioni') ##mostra la lista utenti e i form per promuovere o declassare
@login_required
@admin_required
def authorizations():
	return render_template('gestione_autorizzazioni.html', utenti = richiesta_tabella_utenti())
	

@app.route('/promuovi' , methods =[ "POST"])  ##elabora la promozione di un utente con i dati ricevuti da /autorizzazioni, restituirà un html col risultato dell'operazione
@login_required
@admin_required
def promote():
	u=request.form['id']
	if not u:
		return render_template('risultato.html' , result = False, link = '/autorizzazioni',msg="Inserire un ID")
	resultq = promuovi(int(u))
	return render_template('risultato.html' , result = resultq, link = '/autorizzazioni')

		
@app.route('/declassa' , methods =[ "POST"])  ##elabora il declassamento di un utente con i dati ricevuti da /autorizzazioni, restituirà un html col risultato dell'operazione
@login_required
@admin_required
def downgrade():
	u=request.form['id']
	if not u:
		return render_template('risultato.html' , result = False, link = '/autorizzazioni',msg="Inserire un ID")
	resultq = licenzia(int(u))
	return render_template('risultato.html' , result = resultq, link = '/autorizzazioni')

		
@app.route('/gestisci_proiezioni') ##mostra le proiezioni ancora disponibili dando la possibilità di aggiungerne o chiuderne
@login_required
@gestore_required
def manage_projection():
	return render_template('gestione_proiezioni.html', proiezioni = richiesta_tabella_proiezioni(True) , film = richiesta_tabella_film(False) , sale = richiesta_tabella_sale() ) 
	
		
@app.route('/aggiungi_proiezione' , methods =[ "POST"]) ##elabora la richiesta di aggiungere una nuova proiezione da /gestisci_proiezioni , restituirà un html col risultato dell'operazione
@login_required
@gestore_required
def add_projection():
	anno = request.form['anno']
	mese = request.form['mese']
	giorno = request.form['giorno']
	ora = request.form['ora']
	if(ora==""): #in pratica non è stato messo un orario
		return render_template("risultato.html", result=False , link="/gestisci_proiezioni" , msg="Impostare ora corretta")
	t = ora.split(":")
	data = datetime.datetime(int(anno),int(mese),int(giorno), int(t[0]), int(t[1]))
	if( datetime.datetime.now() > data ):
		return render_template("risultato.html", result=False , link="/gestisci_proiezioni"  , msg="Impostare data corretta")
	sala = request.form['sala']
	film = request.form['film']
	if verifica_id_film(film):
		return render_template("risultato.html", result=False , link="/gestisci_proiezioni" , msg="Impostare ID film corretto")
	prezzo = request.form['biglietto']
	d_film = durata_film(film)
	if (controlla_proiezione(data, sala, durata_film(film))):
		return render_template("risultato.html", result=False , link="/gestisci_proiezioni" , msg="Sala occupata")
	else:
		inserimento_proiezione(data,sala,film,prezzo)
		return render_template("risultato.html", result=True , link="/gestisci_proiezioni" , msg="Proiezione inserita correttamente")
	

@app.route('/chiudi_proiezione' , methods =[ "POST"]) ##elabora la richiesta di chiudere le prenotazioni per una proiezione proveniente da /gestisci_proiezioni , restituirà un html col risultato dell'operazione
@login_required
@gestore_required
def close_projection():
	chiave=request.form['chiave']
	resultquery=disabilita_proiezione(chiave)
	if resultquery:
		return render_template("risultato.html", result=resultquery , link="/gestisci_proiezioni", msg="Prenotazione chiusa")	
	return render_template("risultato.html", result=resultquery , link="/gestisci_proiezioni", msg="Proiezione inesistente")	
	

@app.route('/statistiche') ## mostra varie statistiche
@login_required
@gestore_required
def stats():
	return render_template('grafico.html', anni_stats = anni_statistiche(), incasso = 0, vendite = [0,0,0,0,0,0,0,0,0,0,0,0])

@app.route('/statistiche/<anno>') ## mostra varie statistiche
@login_required
@gestore_required
def statss(anno):
	data = statistiche_vendite_annuali(int(anno))
	return render_template('grafico.html', anni_stats = anni_statistiche(), incasso = int(data[1]), vendite = data[0])

@app.route('/personale') ## pagina personale dell'utente dalla quale può controllare i suoi dati, le prenotazioni e fare nuovi prenotazioni
@login_required
def personal():
	##return render_template("area_personale.html", utente=load_user(current_user.get_id()))
	return render_template('personale.html' , profilo = richiesta_utente(current_user.get_id()))##ANCORA DA SISTEMARE!!!!!!!!!!!
	
@app.route('/prenotazioni') ##mostra la lista delle prenotazioni effettuate
@login_required
def prenotazioni():
	prenotazioni_utente=richiesta_prenotazioni_utente(current_user.get_id())
	return render_template('prenotazioni.html', dati=prenotazioni_utente )
	
@app.route('/prenotabili') ##mostra tutte le proiezioni prenotabili e dà un form per effettuare una prenotazione
@login_required
def prenotabili():
	return render_template('scelta_proiezione.html', proiezioni = richiesta_tabella_proiezioni(False), generi=richiesta_generi_disponibili())

@app.route('/prenotabili/<genere>')
@login_required
def prenotabili_genere(genere):
	return render_template('scelta_proiezione.html', proiezioni = richiesta_tabella_proiezioni_genere(genere), generi=richiesta_generi_disponibili())
	

@app.route('/prenota', methods =[ "POST"]) ##elabora la prenotazione, restituirà un html col risultato dell'operazione
@login_required
def prenota():
	chiave=request.form['chiave']
	occupati = array_posti_prenotati(chiave)
	posti = array_posti_sala(chiave)
	disponibili=[]
	if posti != None:
		for posto in posti:
			if not(posto[0] in occupati):
				disponibili.append(posto)
		quantità=list(range(0,len(disponibili)))
	session['proiezione']=chiave
	return render_template('posti.html', posti=disponibili)

@app.route('/prenotamento', methods =[ "POST"])
@login_required
def prenotamento():
	if ('proiezione' in session) and (request.method == 'POST'):
		proiezione=session['proiezione']
		prenotati=request.form['posti']
		#posti, proiezione, cliente, num_posti
		id=current_user.get_id()
		numero_posti=len(prenotati.split("-"))-1
		inserisci_prenotazione(prenotati, proiezione, id, numero_posti)
		return render_template("risultato.html", result=True , link='/prenotazioni')
	return render_template("risultato.html", result=False , link='/prenota')	
		

	

