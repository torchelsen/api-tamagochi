from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Child, Parent, db

child_blueprint = Blueprint("child", __name__, url_prefix="/child")
def init_app(app):
    # Your initialization logic here
    app.register_blueprint(child_blueprint)

@child_blueprint.route("/get_child/<int:child_id>", methods=["GET"])
@login_required
def get_child(child_id):
    try:
        child = Child.query.get(child_id)

        if not child:
            return jsonify(status=404, message="Criança não encontrada.")

        child_data = {
            "id": child.id,
            "name": child.name,
            "surname": child.surname,
            "gender": child.gender,
            "parent_id": child.parent_id,
        }

        return jsonify(status=200, child=child_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter criança.", error=str(e))
    
@child_blueprint.route("/get_all_children", methods=["GET"])
@login_required
def get_all_children():
    try:
        all_children = Child.query.all()

        children_data = [{
            "id": child.id,
            "name": child.name,
            "surname": child.surname,
            "gender": child.gender,
            "parent_id": child.parent_id,
            # Adicione mais campos conforme necessário
        } for child in all_children]

        return jsonify(status=200, children=children_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as crianças.", error=str(e))

@child_blueprint.route("/update_child/<int:child_id>", methods=["PUT"])
@login_required
def update_child(child_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        child = Child.query.get(child_id)

        if not child:
            return jsonify(status=404, message="Criança não encontrada.")

        # Atualiza os campos da criança com os novos dados
        child.name = data.get("name", child.name)
        child.surname = data.get("surname", child.surname)
        child.gender = data.get("gender", child.gender)

        db.session.commit()

        return jsonify(status=200, message="Criança atualizada com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar criança.", error=str(e))

@child_blueprint.route("/delete_child/<int:child_id>", methods=["DELETE"])
@login_required
def delete_child(child_id):
    try:
        child = Child.query.get(child_id)

        if not child:
            return jsonify(status=404, message="Criança não encontrada.")

        db.session.delete(child)
        db.session.commit()

        return jsonify(status=200, message="Criança excluída com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir criança.", error=str(e))