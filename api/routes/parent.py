from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Parent, Child, Task, db
from datetime import time
from dateutil.parser import parse as date_parse

parent_blueprint = Blueprint("parent", __name__, url_prefix="/parent")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(parent_blueprint)

# LISTA UM PARENT PELO ID
@parent_blueprint.route("/get_parent/<int:parent_id>", methods=["GET"])
def get_parent(parent_id):
    try:
        parent = Parent.query.get(parent_id)

        if parent:
            parent_data = {
                "id": parent.id,
                "name": parent.name,
                "surname": parent.surname,
                "email": parent.email,
                "gender": parent.gender,
                "children": [
                        {
                            "id": child.id,
                            "name": child.name,
                            "surname": child.surname,
                            "gender": child.gender,
                        }
                        for child in parent.children
                    ],
        }

        return jsonify(status=200, parent=parent_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter parent.", error=str(e))
   
# LISTA TODOS OS PARENTS 
@parent_blueprint.route("/get_all_parents", methods=["GET"])
def get_all_parents():
    try:
        all_parents = Parent.query.all()

        parent_data = [{
            "id": parent.id,
            "name": parent.name,
            "surname": parent.surname,
            "email": parent.email,
            "gender": parent.gender,
            "children": [
                        {
                            "id": child.id,
                            "name": child.name,
                            "surname": child.surname,
                            "gender": child.gender,
                        }
                        for child in parent.children
                    ],
        } for parent in all_parents]

        return jsonify(status=200, parents=parent_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas os parents.", error=str(e))

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

    return jsonify(status=200, message="Filho adicionado com sucesso.", child_id=f"{new_child.id}")

@parent_blueprint.route("/create_task", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    
    required_fields = ["name", "description", "start_date", "duration", "day"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="Task inválida ou dados faltando."), 400

    try:
        start_time = date_parse(data["start_date"])
        duration_str = data["duration"]
        duration_hours, duration_minutes = map(int, duration_str.split(':'))
        duration_time = time(hour=duration_hours, minute=duration_minutes)

        day = data["day"]

        parent_task = Task(
            name=data["name"],
            description=data["description"],
            start_date=start_time,
            duration=duration_time,
            day=day,
            is_visible=data.get("is_visible", True),
            is_repeatable=data.get("is_repeatable"),
            task_parent_id=None
        )

        db.session.add(parent_task)
        db.session.commit()

        task_parent_id = parent_task.id

        repeat_days = data.get("repeat_days", [])
        if day not in repeat_days:  
            repeat_days.append(day)

        task_instances = []
        for repeat_day in repeat_days:
            if repeat_day != day:
                new_task = Task(
                    name=data["name"],
                    description=data["description"],
                    start_date=start_time,
                    duration=duration_time,
                    day=repeat_day,
                    is_visible=data.get("is_visible", True),
                    is_repeatable=data.get("is_repeatable"),
                    task_parent_id=task_parent_id
                )
                task_instances.append(new_task)

        db.session.add_all(task_instances)
        db.session.commit()

        return jsonify(status=200, message="Tarefas criadas com sucesso.", task_id=f"{parent_task.id}")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao criar as tarefas.", error=str(e))

# ATRIBUI TASK A CHILD
@parent_blueprint.route("/assign_task_to_child", methods=["POST"])
@login_required
def assign_task_to_child():
    try:
        data = request.get_json()

        if not data or any(field not in data for field in ["task_id"]):
            return jsonify(status=400, message="Dados inválidos ou incompletos.")

        child_id = None
        children = current_user.children
        if children:
            child_id = children[0].id

        task_id = data["task_id"]

        child = Child.query.get(child_id)
        task = Task.query.get(task_id)

        if not child or not task:
            return jsonify(status=400, message="Criança ou tarefa não encontrada.")

        child_tasks = Task.query.filter_by(task_parent_id=task_id).all()
        if child_tasks:
            for child_task in child_tasks:
                task_id = child_task.id
                child.tasks.append(child_task)

        child.tasks.append(task)
        db.session.commit()

        return jsonify(status=200, message="Tarefa atribuída à criança com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atribuir tarefa à criança.", error=str(e))