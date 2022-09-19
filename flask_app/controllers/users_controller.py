from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.appointments import Cita

#Importación BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/') #Pagina principal renderizando index
def index():
    return render_template('index.html')

@app.route('/registrate', methods=['POST'])
def registrate():
    #Validar la información ingresada
    if not User.valida_usuario(request.form): #User es la clase con 
    #la static metod para validar inforamcion del formulario.
    #Si esto es falso la informacion redirigir al inicio
        return redirect('/')
    #Aca se encripta la contraseña.
    pwd = bcrypt.generate_password_hash(request.form['password']) #Encriptamos el password del usuario

    #formulario que se va a estar comparando con el request.form 
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    #request.form = FORMULARIO HTML
    id = User.save(formulario) #Recibo el identificador de mi nuevo usuario

    session['user_id'] = id #Se guarda en sesion el id de usuario.

    return redirect('/dashboard') #Se retorna

@app.route('/login', methods=['POST'])
def login():
    #Verificar que el email EXISTA
    #request.form RECIBIMOS DE HTML
    #request.form = {email: elena@cd.com, password: 123}
    user = User.get_by_email(request.form) #Recibiendo una instancia de usuario o Falso

    if not user: #Si no hay nada en usuario.
        flash('E-mail no encontrado', 'login')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id

    return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)
    citas = Cita.show(formulario)
    dia = Cita.hora()

    return render_template('dashboard.html', user = user, citas = citas, dia = dia)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')