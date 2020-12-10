from flask import * #provaaaaaacazzo
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

@app.route('/')
def home():
	if is_authenticated() and is_admin(load_user(get_id())):
		return redirect("/gestore")
	else: 
		return render_template("home.html")


@app.route('/accedi')
def access()
	return render_template("accesso.html")

@app.route ("/login", methods =[ "POST"])
def logger():
	mail=request.form['email']
	pwd=request.form['password']
	id_ricevuto = verifica_credenziali(mail,pwd)
	if( id_ricevuto >= 0):
		login_user(load_user(id_ricevuto))
		redirect("/personale")
			
	#controllo e login #query login
	return redirect('/')

@app.route('/registrati')
def register()
	return render_template("registrazione.html")

@app.route('/registrazione', methods =[ "POST"])
def registerer()
	
	
@app.route('/gestione')
@login_required
def gestore():
	if is_admin(load_user(get_id())) :
		return render_template('gestione.html')
	else:
			#accesso negato	
			
@app.route('/gestisci_film')
@login_required

@app.route('/aggiungi_film')
@login_required

@app.route('/rimuovi_film')
@login_required	

@app.route('/autorizzazioni')
@login_required

@app.route('/aggiungi_proiezione')
@login_required

@app.route('/statistiche')
@login_required



@app.route('/personale')
@login_required
def personal():
	return render_template("area_personale.html",load_user(get_id()))

@app.route('/prenotazioni')
@login_required
def bookings():
	return render_template("prenotazioni.html",prenotazioni_utente(get_id()))

@app.route('/programmazione')
def programmazione()
	#se loggato torna aggiunge nella pagina l'opzione per prenotare

@app.route('/prenota', proiezione_id)
@login_required
def prenota():
	

