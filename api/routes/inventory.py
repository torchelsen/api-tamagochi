from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Inventory, db


inventory_blueprint = Blueprint("inventory", __name__, url_prefix="/inventory")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(inventory_blueprint)


@inventory_blueprint.route("/add_to_inventory", methods=["POST"])
@login_required
def add_to_inventory():
    data = request.get_json()
    
    child_id = None
    children = current_user.children
    if children:
        child_id = children[0].id

    if not child_id:
        return jsonify(status=400, message="Nenhuma criança encontrada."), 400
    required_fields = ["item_id"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="Inventory inválido ou dados faltando."), 400

    new_inventory = Inventory(
        child_id=child_id,
        item_id=data["item_id"]
    )

    db.session.add(new_inventory)
    db.session.commit()

    return jsonify(status=200, message="Inventory criado com sucesso.")

@inventory_blueprint.route("/get_inventory/<int:inventory_id>", methods=["GET"])
@login_required
def get_inventory(inventory_id):
    try:
        inventory = Inventory.query.get(inventory_id)
        
        if not inventory:
            return jsonify(status=404, message="Inventory não encontrado.")
        
        if not current_user.children:
            return jsonify(status=400, message="Você não tem possui nenhum filho cadastrado."), 400
        
        if inventory.child_id != current_user.children[0].id:
            return jsonify(status=403, message="Você não tem permissão para visualizar este inventory."), 403
        
        inventory_data = {
            "id": inventory.id,
            "child_id": inventory.child_id,
            "item_id": inventory.item_id,
        }

        return jsonify(status=200, inventory=inventory_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter inventory.", error=str(e))

@inventory_blueprint.route("/get_all_inventories_by_child", methods=["GET"])
@login_required
def get_all_inventories():
    try:
        child_id = None
        children = current_user.children
        if children:
            child_id = children[0].id

        all_inventories = Inventory.query.filter_by(child_id=child_id).all()

        inventory_data = [{
            "id": inventory.id,
            "child_id": inventory.child_id,
            "item_id": inventory.item_id,
        } for inventory in all_inventories]

        return jsonify(status=200, inventory=inventory_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas os inventories.", error=str(e))


@inventory_blueprint.route("/update_inventory/<int:inventory_id>", methods=["PUT"])
@login_required
def update_inventory(inventory_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        inventory = Inventory.query.get(inventory_id)

        if not current_user.children:
            return jsonify(status=400, message="Você não tem possui nenhum filho cadastrado."), 400

        if not inventory:
            return jsonify(status=404, message="Inventory não encontrado.")
        
        if inventory.child_id != current_user.children[0].id:
            return jsonify(status=403, message="Você não tem permissão para editar este inventário."), 403

        inventory.item_id = data.get("item_id", inventory.item_id)

        db.session.commit()

        return jsonify(status=200, message="Inventory atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar Inventory.", error=str(e))

@inventory_blueprint.route("/delete_inventory/<int:inventory_id>", methods=["DELETE"])
@login_required
def delete_inventory(inventory_id):
    try:
        inventory = Inventory.query.get(inventory_id)

        if not current_user.children:
            return jsonify(status=400, message="Você não tem possui nenhum filho cadastrado."), 400

        if not inventory:
            return jsonify(status=404, message="Inventory não encontrado.")
        
        if inventory.child_id != current_user.children[0].id:
            return jsonify(status=403, message="Você não tem permissão para deletar este inventário."), 403

        db.session.delete(inventory)
        db.session.commit()

        return jsonify(status=200, message="Inventory excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir inventory.", error=str(e))

