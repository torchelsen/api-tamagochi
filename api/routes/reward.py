from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Reward, db


reward_blueprint = Blueprint("reward", __name__, url_prefix="/reward")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(reward_blueprint)


@reward_blueprint.route("/create_reward", methods=["POST"])
@login_required
def create_reward():
    data = request.get_json()
    
    required_fields = ["type", "value", "description"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="Reward inválido ou dados faltando."), 400

    new_reward = Reward(
        type=data["type"],
        value=data["value"],
        description=data["description"]
    )

    db.session.add(new_reward)
    db.session.commit()

    return jsonify(status=200, message="Reward criado com sucesso.")

@reward_blueprint.route("/get_reward/<int:reward_id>", methods=["GET"])
@login_required
def get_reward(reward_id):
    try:
        reward = Reward.query.get(reward_id)
        
        if not reward:
            return jsonify(status=404, message="Reward não encontrado.")
        
        reward_data = {
            "id": reward.id,
            "type": reward.type,
            "value": reward.value,
            "description": reward.description,
        }

        return jsonify(status=200, reward=reward_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter reward.", error=str(e))

@reward_blueprint.route("/get_all_rewards", methods=["GET"])
@login_required
def get_all_rewards():
    try:
        all_rewards = Reward.query.all()

        reward_data = [{
            "id": reward.id,
            "type": reward.type,
            "value": reward.value,
            "description": reward.description
        } for reward in all_rewards]

        return jsonify(status=200, reward=reward_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todos os rewards.", error=str(e))


@reward_blueprint.route("/update_reward/<int:reward_id>", methods=["PUT"])
@login_required
def update_reward(reward_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        reward = Reward.query.get(reward_id)

        if not reward:
            return jsonify(status=404, message="Reward não encontrado.")
        
        reward.type = data.get("type", reward.type)
        reward.value = data.get("value", reward.value)
        reward.description = data.get("description", reward.description)

        db.session.commit()

        return jsonify(status=200, message="Reward atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar reward.", error=str(e))

@reward_blueprint.route("/delete_reward/<int:reward_id>", methods=["DELETE"])
@login_required
def delete_reward(reward_id):
    try:
        reward = Reward.query.get(reward_id)

        if not reward:
            return jsonify(status=404, message="Reward não encontrado.")
        
        db.session.delete(reward)
        db.session.commit()

        return jsonify(status=200, message="Reward excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir reward.", error=str(e))

