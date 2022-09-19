from flask_app.config.mysqlconnection import  connectToMySQL
from datetime import datetime

from flask import flash

class Cita:
    def __init__(self,data):
        self.id = data['id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO appointments (task, date, status, user_id) VALUES (%(task)s, %(date)s, %(status)s, %(user_id)s)"
        result = connectToMySQL('citas').query_db(query, formulario) #me regresan el nuevo ID de la persona registrada
        #result = 5
        return result

    @staticmethod
    def valida_cita(formulario): 

        es_valido = True 

        if formulario['task'] == "":
            flash('Ingrese task', 'create')
            es_valido = False

        if formulario['date'] == "":
            flash('Ingrese date', 'create')
            es_valido = False
        
        if formulario['status'] == "":
            flash('Ingrese status', 'create')
            es_valido = False
        
        return es_valido

    @classmethod
    def show(cls, formulario):
        query = "SELECT appointments.*, task FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE users.id = %(id)s"
        results = connectToMySQL('citas').query_db(query, formulario)

        citas = []

        for x in results:
            citas.append(cls(x))
        return citas
    
    @classmethod
    def get_by_id(cls, formulario): 
        query = "SELECT appointments.*, task FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE appointments.id = %(id)s"
        #       "SELECT appointments.*, task FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE users.id = %(id)s"
        result = connectToMySQL('citas').query_db(query, formulario) 
        cita = cls(result[0])
        return cita


    @classmethod
    def update(cls, formulario):
        query = "UPDATE appointments SET task=%(task)s, date=%(date)s, status=%(status)s, user_id=%(user_id)s WHERE id = %(id)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): #Recibe formulario con id de receta a borrar
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result

    @staticmethod
    def hora():
        now = datetime.now()
        Fecha = now.date()
        return Fecha

    
