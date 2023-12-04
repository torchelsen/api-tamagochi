from flask import Blueprint, jsonify, request
from flask_login import login_user, login_required, logout_user
from database.models import db, Parent
from flask_bcrypt import Bcrypt

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")
bcrypt = Bcrypt()

def init_app(app):
    bcrypt.init_app(app)
    app.register_blueprint(auth_blueprint)

# CADASTRO
@auth_blueprint.route("/register", methods=["POST"])
def create():
    data = request.get_json()

    if not data or any(field not in data for field in ["name", "surname", "email", "password", "gender"]):
        return jsonify(status=400, message="Dados inválidos ou incompletos.")

    hashed_password = bcrypt.generate_password_hash(data["password"])
    new_user = Parent(name=data["name"], surname=data["surname"], email=data["email"],
                      password=hashed_password, gender=data["gender"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify(status=200, message="Usuário registrado com sucesso!")

# LOGIN
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or any(field not in data for field in ["email", "password"]):
        return jsonify(status=400, message="Email ou senha inválidos.")

    user = Parent.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        login_user(user)
        return jsonify(status=200, message="Logado com sucesso.", user_id=f"{user.id}")
    else:
        return jsonify(status=400, message="Email ou senha inválidos.")

# LOGOUT
@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    try:
        logout_user()
        return jsonify(status=200, message="Logout realizado com sucesso.")
    except:
        return jsonify(status=400, message="Error")
