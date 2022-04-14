import os
from webbrowser import get       #permite accedera ciertas funciones del sistema operativo, para este caso las variables de entorno
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(    #permite definir variables de configuracion
        SECRET_KEY =  'mikey',          #permite definir las sesiones ()
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )

    from . import db
    db.init_app(app)
    
    from .import auth
    from .import todo

    app.register_blueprint(auth.bp) #registramo el blueprint
    app.register_blueprint(todo.bp) #registramo el blueprint
    
    @app.route('/hola')
    def hola():
        return 'hola pagina web'

    return app