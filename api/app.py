import os
from flask import Flask, redirect
from flask import render_template
from sqlalchemy.exc import SQLAlchemyError
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint
from routes.task import init_app as init_task_app
from routes.parent import init_app as init_parent_app
from routes.auth import init_app as init_auth_app
from routes.child import init_app as init_child_app
from routes.item import init_app as init_item_app
from routes.tamagochi import init_app as init_tamagochi_app
from routes.style_tamagochi import init_app as init_style_tamagochi_app
from routes.inventory import init_app as init_inventory_app
from routes.reward import init_app as init_reward_app
from routes.task_reward import init_app as init_task_reward_app
from routes.log_reward import init_app as init_log_reward_app
from routes.child_task import init_app as init_child_task_app
from routes.log_reward import init_app as init_log_reward_app
from routes.mood import init_app as init_mood_app
from routes.log_mood import init_app as init_log_mood_app
from database.models import Parent, db, app
from flask_login import LoginManager, login_manager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'
instance_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_dir, "database.db")}'

# Inicialização do banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    try:
        return Parent.query.get(int(user_id))
    except SQLAlchemyError as e:
        print(f"Error loading user: {e}")
        return None

# Inicialização de blueprints
init_auth_app(app)
init_parent_app(app)
init_child_app(app)
init_task_app(app)
init_item_app(app)
init_tamagochi_app(app)
init_style_tamagochi_app(app)
init_inventory_app(app)
init_reward_app(app)
init_task_reward_app(app)
init_child_task_app(app)
init_log_reward_app(app)
init_mood_app(app)
init_log_mood_app(app)

@app.route("/", methods=["GET"])
def sendToDocs():
    return redirect("/docs")

FLASK_ROUTE = "/docs"
SWAGGER_FILE = "/static/swagger.yml"

swaggerui = get_swaggerui_blueprint(FLASK_ROUTE, SWAGGER_FILE)
app.register_blueprint(swaggerui)

if __name__ == "__main__":
    app.run(debug=True)
