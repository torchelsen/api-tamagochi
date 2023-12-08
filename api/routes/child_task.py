from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import ChildTask, Child, Task, TaskReward, db

child_task_blueprint = Blueprint("child_task", __name__, url_prefix="/child_task")
def init_app(app):
    # Your initialization logic here
    app.register_blueprint(child_task_blueprint)

@child_task_blueprint.route("/get_child_task/<int:child_task_id>", methods=["GET"])
@login_required
def get_child_task(child_task_id):
    try:
        child_task = ChildTask.query.get(child_task_id)

        if not child_task:
            return jsonify(status=404, message="Criança não encontrada.")

        child_task_data = {
            "id": child_task.id,
            "child_id": child_task.child_id,
            "task_id": child_task.task_id,
            "done": child_task.done,
        }

        return jsonify(status=200, child_task=child_task_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter criança.", error=str(e))
    
@child_task_blueprint.route("/get_all_child_tasks", methods=["GET"])
@login_required
def get_all_child_tasks():
    try:
        all_child_task = ChildTask.query.all()

        child_task_data = [{
            "id": child_task.id,
            "child_id": child_task.child_id,
            "task_id": child_task.task_id,
            "done": child_task.done,
        } for child_task in all_child_task]

        return jsonify(status=200, child_task=child_task_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as crianças.", error=str(e))

@child_task_blueprint.route("/update_child_task/<int:child_task_id>", methods=["PUT"])
@login_required
def update_child_task(child_task_id):
    try:
        data = request.get_json()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        child_task = ChildTask.query.get(child_task_id)

        if not child_task:
            return jsonify(status=404, message="ChildTask não encontrado..")

        task = Task.query.get(data["task_id"])

        if not task:
            return jsonify(status=404, message="Task não encontrada.")

        child_id = data["child_id"]
        child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()

        if not child:
            return jsonify(status=404, message="Criança não encontrada.")

        child_task.child_id = data.get("task_id", child_task.task_id)
        child_task.task_id = data.get("child_id", child_task.task_id)
        child_task.done = data.get("done", child_task.done)

        db.session.commit()

        return jsonify(status=200, message="ChildTask atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar ChildTask.", error=str(e))

@child_task_blueprint.route("/delete_child_task/<int:child_task_id>", methods=["DELETE"])
@login_required
def delete_child_task(child_task_id):
    try:
        child_task = ChildTask.query.get(child_task_id)

        if not child_task:
            return jsonify(status=404, message="ChildTask não encontrado.")

        db.session.delete(child_task)
        db.session.commit()

        return jsonify(status=200, message="ChildTask excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir ChildTask.", error=str(e))