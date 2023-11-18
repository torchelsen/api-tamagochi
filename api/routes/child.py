from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Child, Parent, db

child_blueprint = Blueprint("child", __name__, url_prefix="/child")


@child_blueprint.route("/get_child", methods=["GET"])
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
    
@child_blueprint.route("/get_all_childs", methods=["GET"])
@login_required
def get_all_childs():
    try:
        all_childs = Child.query.all()

        childs_data = [{
            "id": child.id,
            "name": child.name,
            "surname": child.surname,
            "gender": child.gender,
            "parent_id": child.parent_id,
            # Adicione mais campos conforme necessário
        } for child in all_childs]

        return jsonify(status=200, childs=childs_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as crianças.", error=str(e))

@child_blueprint.route("/update_child", methods=["PUT"])
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

@child_blueprint.route("/delete_child", methods=["DELETE"])
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