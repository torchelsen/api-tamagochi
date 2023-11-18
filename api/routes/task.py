from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Child, Task, db, ChildTask


task_blueprint = Blueprint("task", __name__)


@task_blueprint.route("/get_task/<int:task_id>", methods=["GET"])
@login_required
def get_task(task_id):
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify(status=404, message="Tarefa não encontrada.")

        task_data = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "period": task.period,
            "frequency": task.frequency,
            "is_visible": task.is_visible,
            "version": task.version,
        }

        return jsonify(status=200, task=task_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter tarefa.", error=str(e))

@task_blueprint.route("/get_all_tasks", methods=["GET"])
@login_required
def get_all_tasks():
    try:
        all_tasks = Task.query.all()

        tasks_data = [{
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "period": task.period,
            "frequency": task.frequency,
            "is_visible": task.is_visible,
            "version": task.version,
        } for task in all_tasks]

        return jsonify(status=200, tasks=tasks_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as tarefas.", error=str(e))

@task_blueprint.route("/update_task/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        task = Task.query.get(task_id)

        if not task:
            return jsonify(status=404, message="Tarefa não encontrada.")

        # Atualiza os campos da tarefa com os novos dados
        task.name = data.get("name", task.name)
        task.description = data.get("description", task.description)
        task.period = data.get("period", task.period)
        task.frequency = data.get("frequency", task.frequency)
        task.is_visible = data.get("is_visible", task.is_visible)

        # Incrementa a versão
        task.version += 1

        db.session.commit()

        return jsonify(status=200, message="Tarefa atualizada com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar tarefa.", error=str(e))

@task_blueprint.route("/delete_task/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify(status=404, message="Tarefa não encontrada.")

        db.session.delete(task)
        db.session.commit()

        return jsonify(status=200, message="Tarefa excluída com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir tarefa.", error=str(e))