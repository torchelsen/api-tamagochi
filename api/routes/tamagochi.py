from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Tamagochi, StyleTamagochi, db


tamagochi_blueprint = Blueprint("tamagochi", __name__, url_prefix="/tamagochi")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(tamagochi_blueprint)


@tamagochi_blueprint.route("/create_tamagochi", methods=["POST"])
@login_required
def create_tamagochi():
    data = request.get_json()
    
    child_id = None
    children = current_user.children
    if children:
        child_id = children[0].id
    else:
        return jsonify(status=400, message="Nenhuma criança cadastrada."), 400

    required_fields = ["name", "growth", "style_tamagochi_id"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="Tamagochi inválido ou dados faltando."), 400

    style_tamagochi_id = data["style_tamagochi_id"]
    style_tamagochi = StyleTamagochi.query.get(style_tamagochi_id)
    if not style_tamagochi:
        return jsonify(status=404, message="StyleTamagochi não encontrado."), 404

    new_tamagochi = Tamagochi(
        name=data["name"],
        growth=data["growth"],
        child_id=child_id,
        style_tamagochi_id=style_tamagochi_id
    )

    db.session.add(new_tamagochi)
    db.session.commit()

    return jsonify(status=200, message="Tamagochi criado com sucesso.")

@tamagochi_blueprint.route("/get_tamagochi/<int:tamagochi_id>", methods=["GET"])
@login_required
def get_tamagochi(tamagochi_id):
    try:
        tamagochi = Tamagochi.query.get(tamagochi_id)
        
        if not tamagochi:
            return jsonify(status=404, message="Tamagochi não encontrado.")
        
        tamagochi_data = {
            "id": tamagochi.id,
            "name": tamagochi.name,
            "growth": tamagochi.growth,
            "child_id": tamagochi.child_id,
            "style_tamagochi_id": tamagochi.style_tamagochi_id
        }

        return jsonify(status=200, tamagochi=tamagochi_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter tamagochi.", error=str(e))

@tamagochi_blueprint.route("/get_all_tamagochis", methods=["GET"])
@login_required
def get_all_tamagochis():
    try:
        all_tamagochis = Tamagochi.query.all()

        tamagochi_data = [{
            "id": tamagochi.id,
            "name": tamagochi.name,
            "growth": tamagochi.growth,
            "child_id": tamagochi.child_id,
            "style_tamagochi_id": tamagochi.style_tamagochi_id,
        } for tamagochi in all_tamagochis]

        return jsonify(status=200, tamagochi=tamagochi_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as crianças.", error=str(e))


@tamagochi_blueprint.route("/update_tamagochi/<int:tamagochi_id>", methods=["PUT"])
@login_required
def update_tamagochi(tamagochi_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        tamagochi = Tamagochi.query.get(tamagochi_id)

        if not tamagochi:
            return jsonify(status=404, message="Tamagochi não encontrado.")

        tamagochi.name = data.get("name", tamagochi.name)
        tamagochi.growth = data.get("growth", tamagochi.growth)
        tamagochi.style_tamagochi_id = data.get("style_tamagochi_id", tamagochi.style_tamagochi_id)

        db.session.commit()

        return jsonify(status=200, message="Tamagochi atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar Tamagochi.", error=str(e))

@tamagochi_blueprint.route("/delete_tamagochi/<int:tamagochi_id>", methods=["DELETE"])
@login_required
def delete_tamagochi(tamagochi_id):
    try:
        tamagochi = Tamagochi.query.get(tamagochi_id)

        if not tamagochi:
            return jsonify(status=404, message="Tamagochi não encontrado.")

        db.session.delete(tamagochi)
        db.session.commit()

        return jsonify(status=200, message="Tamagochi excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir tamagochi.", error=str(e))

