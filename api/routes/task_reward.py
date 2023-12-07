from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Reward, Task, TaskReward, db


task_reward_blueprint = Blueprint("task_reward", __name__, url_prefix="/task_reward")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(task_reward_blueprint)


@task_reward_blueprint.route("/add_task_reward", methods=["POST"])
@login_required
def add_task_reward():
    data = request.get_json()
    
    required_fields = ["reward_id", "task_id"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="TaskReward inválido ou dados faltando."), 400

    reward = Reward.query.get(data["reward_id"])
    task = Task.query.get(data["task_id"])

    if not reward or not task:
        return jsonify(status=400, message="Reward ou task não encontrados."), 400

    new_task_reward = TaskReward(
        reward_id=data["reward_id"],
        task_id=data["task_id"],
    )

    db.session.add(new_task_reward)
    db.session.commit()

    return jsonify(status=200, message="TaskReward criado com sucesso.")

@task_reward_blueprint.route("/get_task_reward/<int:task_reward_id>", methods=["GET"])
@login_required
def get_task_reward(task_reward_id):
    try:
        task_reward = TaskReward.query.get(task_reward_id)
        
        if not task_reward:
            return jsonify(status=404, message="TaskReward não encontrado.")
        
        task_reward_data = {
            "id": task_reward.id,
            "reward_id": task_reward.reward_id,
            "task_id": task_reward.task_id
        }

        return jsonify(status=200, task_reward=task_reward_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter task_reward.", error=str(e))

@task_reward_blueprint.route("/get_all_task_rewards", methods=["GET"])
@login_required
def get_all_task_rewards():
    try:
        all_task_rewards = TaskReward.query.all()

        task_reward_data = [{
            "id": task_reward.id,
            "reward_id": task_reward.reward_id,
            "task_id": task_reward.task_id
        } for task_reward in all_task_rewards]

        return jsonify(status=200, task_reward=task_reward_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todos os task_rewards.", error=str(e))


@task_reward_blueprint.route("/update_task_reward/<int:task_reward_id>", methods=["PUT"])
@login_required
def update_task_reward(task_reward_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        task_reward = TaskReward.query.get(task_reward_id)

        if not task_reward:
            return jsonify(status=400, message="TaskReward não encontrado."), 400
        
        task_reward.reward_id = data.get("reward_id", task_reward.reward_id)
        task_reward.task_id = data.get("task_id", task_reward.task_id)

        db.session.commit()

        return jsonify(status=200, message="TaskReward atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar task_reward.", error=str(e))

@task_reward_blueprint.route("/delete_task_reward/<int:task_reward_id>", methods=["DELETE"])
@login_required
def delete_task_reward(task_reward_id):
    try:
        task_reward = TaskReward.query.get(task_reward_id)

        if not task_reward:
            return jsonify(status=404, message="TaskReward não encontrado.")
        
        db.session.delete(task_reward)
        db.session.commit()

        return jsonify(status=200, message="TaskReward excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir task_reward.", error=str(e))

