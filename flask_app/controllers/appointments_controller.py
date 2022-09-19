from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación del modelo
from flask_app.models.users import User
from flask_app.models.appointments import Cita

@app.route('/new/appointment')
def show():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }

    user = User.get_by_id(formulario)

    return render_template("new_appointment.html", user = user)

@app.route('/create/appointment', methods = ['POST'])
def saveAppo():

    if 'user_id' not in session:
        return redirect('/')

    if not Cita.valida_cita(request.form): 
        return redirect('/new/appointment')

    id = Cita.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/cita/<int:id>')
def show_edit(id):

    formulario_2 = {'id': id}

    if 'user_id' not in session:
        return redirect('/')

    formulario = {
        'id': session['user_id']
    }
    citas = Cita.get_by_id(formulario_2)
    user = User.get_by_id(formulario)
    return render_template('edit_appointment.html', citas = citas, user = user)

@app.route('/update/appointment', methods = ['POST'])
def update():

    if 'user_id' not in session:
        return redirect('/')
    
    if not Cita.valida_cita(request.form): #llama a la función de valida_receta enviándole el formulario, comprueba que sea valido 
        return redirect('/edit/cita/'+request.form['id'])
    
    Cita.update(request.form)
    return redirect('/dashboard')

@app.route('/delete/cita/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Cita.delete(formulario)

    return redirect('/dashboard')




    





