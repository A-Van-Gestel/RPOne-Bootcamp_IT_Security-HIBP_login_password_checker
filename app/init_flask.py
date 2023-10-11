import os

from flask import Flask

from extensions import db, bcrypt
from utils.configmanager import ConfigManager


class App:
    """
     Singleton: sole static instance of Flask App
    """
    _app_instance = None
    _config_manager_instance = None

    @staticmethod
    def init():
        # Do init once
        if not App._app_instance:
            # Flask constructor
            app = Flask(__name__)

            # Database setup
            basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            sql_path = 'sqlite:///' + os.path.join(basedir, 'database.db')
            print(f'SQL Database location: "{sql_path}"')
            app.config['SQLALCHEMY_DATABASE_URI'] = sql_path
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            db.init_app(app)

            # Bcrypt setup
            bcrypt.init_app(app)

            with app.app_context():
                # ----- Register Models -----
                # noinspection PyUnresolvedReferences
                from models import user
                # ----- Create DB Tables -----
                db.create_all()

            # ----- Register blueprints -----
            # Index page
            from main import bp as main_bp
            app.register_blueprint(main_bp)

            # Finally assign app-instance
            App._app_instance = app
            # ConfigManager
            App._config_manager_instance = ConfigManager.instance()

            # Debug mode
            if App._config_manager_instance.config.getboolean('application', 'debug'):
                app.config['DEBUG'] = True

            # Open on startup
            if App._config_manager_instance.config.getboolean('application', 'open_on_startup') and app.debug is False:
                import webbrowser
                webbrowser.open('http://127.0.0.1:5000', new=2)

            print("FLASK Instance created")

    @staticmethod
    def get_app() -> Flask:
        App.init()
        return App._app_instance

    @staticmethod
    def get_config_manager() -> ConfigManager:
        App.init()
        return App._config_manager_instance
