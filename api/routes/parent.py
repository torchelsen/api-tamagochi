from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Child, Task, db

parent_blueprint = Blueprint("parent", __name__, url_prefix="/parent")

# CRIA CHILD
@parent_blueprint.route("/create_child", methods=["POST"])
@login_required
def create_child():
    data = request.get_json()

    if not data or any(field not in data for field in ["name", "surname", "gender"]):
        return jsonify(status=400, message="Dados inválidos ou incompletos.")

    parent_id = current_user.id
    new_child = Child(name=data["name"], surname=data["surname"], gender=data["gender"], parent_id=parent_id)
    db.session.add(new_child)
    db.session.commit()

    return jsonify(status=200, message="Filho adicionado com sucesso.")


# CRIA TASK
@parent_blueprint.route("/create_task", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    
    if not all(data.get(field) for field in ["name", "description", "period", "frequency"]):
        return jsonify(status=400, message="Task inválida ou dados faltando."), 400

    new_task = Task(
        name=data["name"],
        description=data["description"],
        period=data["period"],
        frequency=data["frequency"],
        is_visible=data.get("is_visible", True)
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(status=200, message="Task criada com sucesso.")

# ATRIBUI TASK A CHILD
@parent_blueprint.route("/assign_task_to_child", methods=["POST"])
@login_required
def assign_task_to_child():
    try:
        data = request.get_json()

        if not data or any(field not in data for field in ["child_id", "task_id"]):
            return jsonify(status=400, message="Dados inválidos ou incompletos.")

        child_id = data["child_id"]
        task_id = data["task_id"]

        child = Child.query.get(child_id)
        task = Task.query.get(task_id)

        if not child or not task:
            return jsonify(status=400, message="Criança ou tarefa não encontrada.")

        child.tasks.append(task)  # Adiciona a tarefa à lista de tarefas da criança
        db.session.commit()

        return jsonify(status=200, message="Tarefa atribuída à criança com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atribuir tarefa à criança.", error=str(e))