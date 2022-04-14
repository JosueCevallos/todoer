from distutils.command.config import config
import mysql.connector
import click        #esta herramienta me permite ejecutar comando en la terminal, para crear tablas y datos
from flask import current_app, g       #current_app mantiene la aplicacion que se esta ejecutando y g es una variable que en global en 
                                        #toda la aplicacion, se usara para almacenar el usuario

from flask.cli import with_appcontext     #permite acceder al usuario y contraseña
from .schema import instructions

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c                #devuelve la base de datos y el conector

#fucnion que cierra la conexion con la base de datos

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)        #el cursos ejecuta cada una de las instrucciones sql que estan en scehma
    
    db.commit()             #las actualiza

@click.command('init-db')   #este es el nombre que debemos utilizar en la terminal cuando vaya a ejecutar la aplicacion 'Flask init-db'
@with_appcontext            #permite accceder a las variables de conexion


def init_db_command():      #para poder esta funcion desde la temrinal, necesito DECORARLA. 
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):      #cuando termine de realizar la peticion
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)