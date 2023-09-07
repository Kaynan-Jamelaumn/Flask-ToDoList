from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
db = SQLAlchemy()
DB_NAME = 'database.sqlite'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '___jamelaumn___DJKpdjoggfpyht#$#dh___ENRICKY___jklfDHFCJFOHY78JTRNDY7FYLIOP0I47a___kaynan___'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # caminho do banco
    
    db.init_app(app)

    migrate = Migrate(app, db)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/account')
    
    from .models import User, Task
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # pra redirecionar pra página de login
    login_manager.login_message = 'Faça o login para acessar essa página'
    login_manager.init_app(app)
    
    @login_manager.user_loader # pra buscar 
    def load_user(user_id):
        return User.query.get(int(user_id))
    # UNCOMMENT ONLY IF YOU WISH TO NOT UTILIZE FLASK MIGRATE
    # with app.app_context():
    #     create_database()
    
    return app # pra passar a referência no main.py

    # UNCOMMENT ONLY IF YOU WISH TO NOT UTILIZE FLASK MIGRATE

# def create_database():
#     if not path.exists('C:\\Users\\Aluno\\Jamelaumn\\Flask\\project3\\project\\instance\\' + DB_NAME):
#         db.create_all()
#         print('Banco criado!')