from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Child, Reward, LogReward, db
from datetime import datetime

log_reward_blueprint = Blueprint("log_reward", __name__, url_prefix="/log_reward")
def init_app(app):
    # Your initialization logic here
    app.register_blueprint(log_reward_blueprint)


@log_reward_blueprint.route("/add_log_reward", methods=["POST"])
@login_required
def add_log_reward():
    data = request.get_json()
    
    now = datetime.now()

    required_fields = ["reward_id", "child_id"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="LogReward inválido ou dados faltando."), 400

    reward = Reward.query.get(data["reward_id"])

    if not reward:
        return jsonify(status=404, message="Reward não encontrado.")

    child_id = data["child_id"]
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()

    if not child:
        return jsonify(status=404, message="Criança não encontrada.")

    new_log_reward = LogReward(
        reward_id=data["reward_id"],
        child_id=data["child_id"],
        timestamp=now
    )

    db.session.add(new_log_reward)
    db.session.commit()

    return jsonify(status=200, message="LogReward criado com sucesso.")

@log_reward_blueprint.route("/get_log_reward/<int:log_reward_id>", methods=["GET"])
@login_required
def get_log_reward(log_reward_id):
    try:
        log_reward = LogReward.query.get(log_reward_id)

        if not log_reward:
            return jsonify(status=404, message="Log não encontrado.")

        log_reward_data = {
            "id": log_reward.id,
            "reward_id": log_reward.reward_id,
            "child_id": log_reward.child_id,
            "timestamp": log_reward.timestamp,
        }

        return jsonify(status=200, log_reward=log_reward_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter Log.", error=str(e))
    
@log_reward_blueprint.route("/get_all_log_rewards", methods=["GET"])
@login_required
def get_all_log_rewards():
    try:
        all_log_rewards = LogReward.query.all()

        log_reward_data = [{
            "id": log_reward.id,
            "reward_id": log_reward.reward_id,
            "child_id": log_reward.child_id,
            "timestamp": log_reward.timestamp,
        } for log_reward in all_log_rewards]

        return jsonify(status=200, log_rewards=log_reward_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as crianças.", error=str(e))

@log_reward_blueprint.route("/update_log_reward/<int:log_reward_id>", methods=["PUT"])
@login_required
def update_log_reward(log_reward_id):
    try:
        data = request.get_json()

        now = datetime.now()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        log_reward = LogReward.query.get(log_reward_id)

        if not log_reward:
            return jsonify(status=404, message="Log não encontrado.")

        reward = Reward.query.get(data["reward_id"])

        if not reward:
            return jsonify(status=404, message="Reward não encontrado.")

        child_id = data["child_id"]
        child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()

        if not child:
            return jsonify(status=404, message="Criança não encontrada.")

        log_reward.reward_id = data.get("reward_id", log_reward.reward_id)
        log_reward.child_id = data.get("child_id", log_reward.child_id)
        log_reward.timestamp = now
        
        db.session.commit()

        return jsonify(status=200, message="Log atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar Log.", error=str(e))

@log_reward_blueprint.route("/delete_log_reward/<int:log_reward_id>", methods=["DELETE"])
@login_required
def delete_log_reward(log_reward_id):
    try:
        log_reward = LogReward.query.get(log_reward_id)

        if not log_reward:
            return jsonify(status=404, message="Log não encontrado.")

        db.session.delete(log_reward)
        db.session.commit()

        return jsonify(status=200, message="Log excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir Log.", error=str(e))