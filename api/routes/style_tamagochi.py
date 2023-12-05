from flask import Blueprint, jsonify, request
from flask_login import login_required
from database.models import StyleTamagochi, db


style_tamagochi_blueprint = Blueprint("style_tamagochi", __name__, url_prefix="/style_tamagochi")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(style_tamagochi_blueprint)


@style_tamagochi_blueprint.route("/add_style_tamagochi", methods=["POST"])
@login_required
def add_style_tamagochi():
    data = request.get_json()
    
    required_fields = ["name"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="style_tamagochi inválido ou dados faltando."), 400

    new_style_tamagochi = StyleTamagochi(
        name=data["name"],
        head=data["head"],
        chest=data["chest"],
        feet=data["feet"],
        glasses=data["glasses"],
        scenario=data["scenario"],
    )

    db.session.add(new_style_tamagochi)
    db.session.commit()

    return jsonify(status=200, message="style_tamagochi criado com sucesso.")

@style_tamagochi_blueprint.route("/get_style_tamagochi/<int:style_tamagochi_id>", methods=["GET"])
@login_required
def get_style_tamagochi(style_tamagochi_id):
    try:
        style_tamagochi = StyleTamagochi.query.get(style_tamagochi_id)
        
        if not style_tamagochi:
            return jsonify(status=404, message="style_tamagochi não encontrado.")
        
        style_tamagochi_data = {
            "id": style_tamagochi.id,
            "name": style_tamagochi.name,
            "head": style_tamagochi.head,
            "chest": style_tamagochi.chest,
            "feet": style_tamagochi.feet,
            "glasses": style_tamagochi.glasses,
            "scenario": style_tamagochi.scenario
        }

        return jsonify(status=200, style_tamagochi=style_tamagochi_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter style_tamagochi.", error=str(e))

@style_tamagochi_blueprint.route("/get_all_style_tamagochis", methods=["GET"])
@login_required
def get_all_style_tamagochis():
    try:
        all_style_tamagochis = StyleTamagochi.query.all()

        style_tamagochi_data = [{
            "id": style_tamagochi.id,
            "name": style_tamagochi.name,
            "head": style_tamagochi.head,
            "chest": style_tamagochi.chest,
            "feet": style_tamagochi.feet,
            "glasses": style_tamagochi.glasses,
            "scenario": style_tamagochi.scenario
        } for style_tamagochi in all_style_tamagochis]

        return jsonify(status=200, style_tamagochi=style_tamagochi_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as crianças.", error=str(e))


@style_tamagochi_blueprint.route("/update_style_tamagochi/<int:style_tamagochi_id>", methods=["PUT"])
@login_required
def update_style_tamagochi(style_tamagochi_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        style_tamagochi = StyleTamagochi.query.get(style_tamagochi_id)

        if not style_tamagochi:
            return jsonify(status=404, message="Style_tamagochi não encontrado.")

        style_tamagochi.name = data.get("name", style_tamagochi.name)
        style_tamagochi.head = data.get("head", style_tamagochi.head)
        style_tamagochi.chest = data.get("chest", style_tamagochi.chest)
        style_tamagochi.feet = data.get("feet", style_tamagochi.feet)
        style_tamagochi.glasses = data.get("glasses", style_tamagochi.glasses)
        style_tamagochi.scenario = data.get("scenario", style_tamagochi.scenario)

        db.session.commit()

        return jsonify(status=200, message="style_tamagochi atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar style_tamagochi.", error=str(e))

@style_tamagochi_blueprint.route("/delete_style_tamagochi/<int:style_tamagochi_id>", methods=["DELETE"])
@login_required
def delete_style_tamagochi(style_tamagochi_id):
    try:
        style_tamagochi = StyleTamagochi.query.get(style_tamagochi_id)

        if not style_tamagochi:
            return jsonify(status=404, message="style_tamagochi não encontrado.")

        db.session.delete(style_tamagochi)
        db.session.commit()

        return jsonify(status=200, message="style_tamagochi excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir style_tamagochi.", error=str(e))

