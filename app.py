from flask import Flask, session, flash, render_template, request, redirect, url_for, abort, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_user , logout_user , current_user , login_required, LoginManager
import requests
import os
import sendgrid


app = Flask(__name__,static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clasificados.db'
app.config['SECRET_KEY'] = os.urandom(24)
sg = sendgrid.SendGridClient('jdelacruz', 'hackPR')
db = SQLAlchemy(app)

dropbox = 'https://console.cloud-elements.com/elements/api-v2/hubs/documents/files'
dropbox_headers = {
	'Authorization': 'User KcpR6dUjc3NAKkpSa6HXZbDF72jd/OrBHsr/rR/loB4=, Organization 2f409265e847e2f8b5332cffe1a8317b, Element fjti2PmI9mH17gL+nl2tZtCMNYWqotP8l/EKtLE/zy4='
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model):
	__tablename__ = "User"
	nombre = db.Column(db.String(50))
	email = db.Column(db.String(20), unique=True)
	telefono = db.Column(db.String(10))
	username = db.Column(db.String(20), unique=True)
	password = db.Column(db.String(15))
	id = db.Column(db.Integer, primary_key=True)
	mercancia = db.relationship("Mercancia", uselist=False, backref="User")

	def __init__(self, nombre, email, telefono, username, password):
		self.nombre = nombre
		self.email = email
		self.telefono = telefono
		self.username = username
		self.password = password

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)

class Mercancia(db.Model):
	__tablename__ = "Mercancia"
	precio = db.Column(db.Float)
	pueblo = db.Column(db.String(15))
	u_id = db.Column(db.Integer, db.ForeignKey('User.id'))
	descripcion = db.Column(db.String(100))
	id = db.Column(db.Integer, primary_key=True)
	transporte = db.relationship("Transporte", uselist=False, backref="Mercancia")
	bienesRaices = db.relationship("BienesRaices", uselist=False, backref="Mercancia")
	mascotas = db.relationship("Mascotas", uselist=False, backref="Mercancia")

	def __init__(self, precio, pueblo, u_id, descripcion):
		self.precio = precio
		self.pueblo = pueblo
		self.u_id = u_id
		self.descripcion = descripcion

class Transporte(db.Model):
	__tablename__ = "Transporte"
	year = db.Column(db.Integer)
	modelo = db.Column(db.String(15))
	marca = db.Column(db.String(15))
	tipot = db.Column(db.String(10))
	m_id = db.Column(db.Integer, db.ForeignKey('Mercancia.id'), primary_key=True)

	def __init__(self, tipot, year, modelo, marca, m_id):
		self.year = year
		self.modelo = modelo
		self.marca = marca
		self.tipot = tipot
		self.m_id = m_id

class BienesRaices(db.Model):
	__tablename__ = "BienesRaices"
	cuartos = db.Column(db.Integer)
	bathrooms = db.Column(db.Integer)
	pisos = db.Column(db.Integer)
	tipobr = db.Column(db.String(10))
	id = db.Column(db.Integer, db.ForeignKey('Mercancia.id'), primary_key=True)

	def __init__(self, tipobr, cuartos, bathrooms, pisos, m_id):
		self.tipobr = tipobr
		self.cuartos = cuartos
		self.bathrooms = bathrooms
		self.pisos = pisos
		self.id = m_id

class Mascotas(db.Model):
	__tablename__ = "Mascotas"
	raza = db.Column(db.String(20))
	cantidad = db.Column(db.Integer)
	macho = db.Column(db.Boolean)
	hembra = db.Column(db.Boolean)
	m_id = db.Column(db.Integer, db.ForeignKey('Mercancia.id'), primary_key=True)

	def __init__(self, tipom ,raza, cantidad, macho, hembra, m_id):
		self.tipom = tipom
		self.raza = raza
		self.cantidad = cantidad
		self.macho = macho
		self.hembra = hembra
		self.m_id = m_id

# db.create_all() 
# db.session.add(User('admin', 'admin@example.com', '7876198346', 'trepi02', 'hackPR'))
# db.session.add(User("Pablo", "pablo@hackpr.io", "7878329932", "pablito", "passpab"))
# db.session.add(User("Sara", "sara@hackpr.io", "7872334754", "sarita", "passsar"))
# db.session.add(User("Pedro", "pedro@hackpr.io", "7872347657", "pedrito", "passped"))
# db.session.add(User("Maria", "maria@hackpr.io", "7870192365", "mariita", "passmar"))
# db.session.add(User("Luis", "luis@hackpr.io", "7875765350", "luisito", "passlui"))
# db.session.add(User("Rosa", "rosa@hackpr.io", "7879080322", "rosita", "passros"))
# db.session.add(User("Carlos", "carlos@hackpr.io", "7879993243", "carlito", "passcar"))
# db.session.add(User("Carla", "carla@hackpr.io", "7872667321", "carlita", "passcar"))
# db.session.add(User("Jose", "jose@hackpr.io", "7872130763", "joseito", "passjos"))
# db.session.add(User("Carmen", "carmen@hackpr.io", "7871243556", "carmensita", "passcar"))
# db.session.commit()


# db.session.add(Mercancia(1000.00, "Carolina", 12, "baba"))
# db.session.add(Mascotas("perro", "PerroCaro", 4, 1, 1, 1))
# db.session.add(Mercancia(1000.00, "San Juan", 2, "baba"))
# db.session.add(Mascotas("perro", "PerroNoSato", 1, 0, 1,2))


# db.session.add(Mercancia(10.00, "Toa Alta", 2, "baba"))
# db.session.add(Mascotas("perro", "Sato", 1, 1, 0,3))
# db.session.add(Mercancia(250.00, "Barceloneta", 3, "baba"))
# db.session.add(Mascotas("perro", "Husky", 1, 0, 1,4))
# db.session.add(Mercancia(7000.00, "San Juan", 4, "baba"))
# db.session.add(Transporte("carro", 2006, "Toyota", "Matrix",5))
# db.session.add(Mercancia(2000.00, "San Juan", 5, "baba"))
# db.session.add(Transporte("carro", 2000, "Toyota", "Barato",6))
# db.session.add(Mercancia(300.00, "Fajardo", 6, "baba"))
# db.session.add(Mascotas("perro", "Pomeranian", 2, 1, 1,7))
# db.session.add(Mercancia(5.78, "Aibonito", 7, "baba"))
# db.session.add(Mascotas("perro", "Satobonito", 1, 1, 0,8))
# db.session.add(Mercancia(5000.00, "Aguada", 8, "baba"))
# db.session.add(Transporte("carro", 2004, "Mitsubishi", "Technica",9))
# db.session.add(Mercancia(20.00, "Mayaguez", 9, "baba"))
# db.session.add(Mascotas("perro", "Dobermansito", 1, 1, 0,10))
# db.session.add(Mercancia(1000000.00, "Ponce", 11, "baba"))
# db.session.add(BienesRaices("mansion", 5, 3, 3,11))
# db.session.add(Mercancia(36000.00, "Ponce", 11, "baba"))
# db.session.add(BienesRaices("casa", 3, 1, 1,12))
# db.session.commit()

# result = db.session.execute("Select m_id from Transporte")
# for row in result:
#     print "username:", row['m_id']

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def index():
	return render_template('index.html', users=User.query.all(), merca = Mercancia.query.all(), 
		transp = Transporte.query.all(), br=BienesRaices.query.all(), masco = Mascotas.query.all())

@app.route("/subefoto", methods = ['POST'])
def subelafoto():
	categoria = request.form['categoria']
	tipo = request.form['tipo']
	precio = request.form['precio']
	descripcion = request.form['message']
	foto = request.files['foto']
	file_dic = {'file': foto}
	db.session.add(Mercancia(precio, "San Juan", 5, descripcion))
	db.session.commit()
	idM = db.session.execute("Select id from Mercancia where descripcion='"+descripcion+"'").fetchone()['id']
	db.session.add(Transporte(tipo, 2000, "Toyota", "Matrix", idM))
	db.session.commit()
	r = requests.post(dropbox+'?path=/Pictures/'+str(idM)+'.jpg&overwrite=true', files=file_dic, headers=dropbox_headers)
	# print r.json()['id']

	# print r.status_code
	return redirect(url_for('articleInfo', id=r.json()['id'], idM = idM))

@app.route("/article")
@login_required
def articleInfo():
	foto_id = request.args['id']
	idM = request.args["idM"]
	r = requests.get(dropbox+'/'+foto_id+'/links', headers=dropbox_headers)
	foto_url = str(r.json()['providerLink'])
	result = db.session.execute("Select descripcion, precio from Mercancia where id='"+str(idM)+"'").fetchone()
	return render_template('article.html', foto_id = foto_id, foto_url=foto_url, descripcion=result['descripcion'], 
		precio=result['precio'])

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('registro.html')

    nombre = request.form['nombre'] + " " + request.form['apellido']
    email = request.form['email']
    telefono = request.form['telefono']
    username = request.form['username']
    password = request.form['password']
         
    user = User(nombre, email, telefono, username, password)

    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('index'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('inicio.html')
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(email=email,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('prof', email=email))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.route('/test')
@login_required
def test():
	return "Hello WOrld!!!"

@app.route('/contact', methods=['GET', 'POST'])
def contacto():
	if request.method == 'GET':
		return render_template('contact-form.html')
	nombre = request.form['name']
	email = request.form['email']
	mensaje = request.form['message']

	message = sendgrid.Mail()
	message.add_to('jjdl_cn@hotmail.com')
	message.set_subject('Example')
	message.set_html('Body')
	message.set_text(mensaje)
	message.set_from('Doe John <doe@email.com>')
	status, msg = sg.send(message)

	return render_template('index.html')

@app.route('/profile')
@login_required
def prof():
	email = request.args['email']
	# result = db.session.execute("Select id, precio,  from User Natural Join Mercancia where email = '" + email + "'")
	# result = db.session.execute("Select id, nombre from User Natural Join Mercancia where email = '" + email + "'")
	# for row in result:
	# 	print 'hola puta'
	# 	print row['id']
	userID = str(g.user.id)
	nombre = db.session.execute("Select nombre from User where id=" + userID).fetchone()['nombre']
	# mercancia = db.session.execute("Select ")
	# print nombre['nombre']
	# return "hola"
	return render_template("profile.html", nombre_usuario = nombre)

@app.route('/br', methods=['GET','POST'])
def bienes():
	if request.method == 'GET':
		print request.query_string
		return render_template('br-search.html')
	
	return "Hellow World"

@app.route("/vender")
def sell():
	return render_template("vender.html")

@app.before_request
def before_request():
    g.user = current_user

if __name__ == "__main__":
	app.run(debug=True)



