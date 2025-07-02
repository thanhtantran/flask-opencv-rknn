import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import config_dict



def setup_log(log_level):
    
    logging.basicConfig(level=log_level)  


    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 10, backupCount=10)

    formatter = logging.Formatter('%(levelname)s %(pathname)s:%(lineno)d %(message)s')

    file_log_handler.setFormatter(formatter)

    logging.getLogger().addHandler(file_log_handler)



def create_app(config_type):  

    config_class = config_dict[config_type]
    app = Flask(__name__)
    app.config.from_object(config_class)


    from controller.modules.home import home_blu
    app.register_blueprint(home_blu)
    from controller.modules.user import user_blu
    app.register_blueprint(user_blu)


    setup_log(config_class.LOG_LEVEL)

    return app
