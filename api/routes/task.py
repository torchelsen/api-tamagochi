from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import  Task, ChildTask, db
from datetime import datetime, time
from dateutil.parser import parse as date_parse

task_blueprint = Blueprint("task", __name__, url_prefix="/task")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(task_blueprint)


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
            "start_date": task.start_date,
            "duration": task.duration.strftime("%H:%M"),
            "day": task.day,
            "is_visible": task.is_visible,
            "is_repeatable": task.is_repeatable,
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
            "start_date": task.start_date,
            "duration": task.duration.strftime("%H:%M"),
            "day": task.day,
            "is_visible": task.is_visible,
            "is_repeatable": task.is_repeatable,
            "task_parent_id": task.task_parent_id
        } for task in all_tasks]

        return jsonify(status=200, tasks=tasks_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas as tarefas.", error=str(e))

@task_blueprint.route("/update_task/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    try:
        data = request.get_json()
        start_time = datetime.fromisoformat(data["start_date"])
        duration_str = data["duration"]
        duration_hours, duration_minutes = map(int, duration_str.split(':'))
        duration_time = time(hour=duration_hours, minute=duration_minutes)

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        task = Task.query.get(task_id)

        if not task:
            return jsonify(status=404, message="Tarefa não encontrada.")

        # Atualiza os campos da tarefa com os novos dados
        task.name = data.get("name", task.name)
        task.description = data.get("description", task.description)
        task.start_date = start_time
        task.duration = duration_time
        task.day = data.get("day", task.day)
        task.is_visible = data.get("is_visible", task.is_visible)
        task.is_repeatable = data.get("is_repeatable", task.is_repeatable)

        # Incrementa a versão
        task.version += 1

        db.session.commit()

        return jsonify(status=200, message="Tarefa atualizada com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar tarefa.", error=str(e))
    

@task_blueprint.route("/update_all_tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_all_tasks(task_id):
    try:
        data = request.get_json()
        start_time = datetime.fromisoformat(data["start_date"])
        duration_str = data["duration"]
        duration_hours, duration_minutes = map(int, duration_str.split(':'))
        duration_time = time(hour=duration_hours, minute=duration_minutes)

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        task = Task.query.get(task_id)

        if not task:
            return jsonify(status=404, message="Tarefa não encontrada.")

        # Atualiza os campos da tarefa com os novos dados
        task.name = data.get("name", task.name)
        task.description = data.get("description", task.description)
        task.start_date = start_time
        task.duration = duration_time
        task.is_visible = data.get("is_visible", task.is_visible)

        task.version += 1

        # Encontrar a tarefa pai, se existir
        parent_task_id = task.task_parent_id
        if parent_task_id:
            parent_task = Task.query.get(parent_task_id)
            if parent_task:
                
                parent_task.name = task.name
                parent_task.description = task.description
                parent_task.start_date = task.start_date
                parent_task.duration = task.duration
                parent_task.is_visible = task.is_visible

                parent_task.version += 1

        # Recupera todas as tarefas filhas e as atualiza com os mesmos dados
        child_tasks = Task.query.filter_by(task_parent_id=task_id).all()
        for child_task in child_tasks:
            child_task.name = task.name
            child_task.description = task.description
            child_task.start_date = task.start_date
            child_task.duration = task.duration
            child_task.is_visible = task.is_visible
            child_task.parent_task_id = task_id
            child_task.version += 1

        db.session.commit()

        return jsonify(status=200, message="Tarefa e tarefas filhas atualizadas com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar tarefa e tarefas filhas.", error=str(e))


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
    

@task_blueprint.route("/delete_all_tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_all_tasks(task_id):
    try:
        tasks_to_delete = [task_id]
        deleted_tasks = set()

        # Encontrar todas as tarefas filhas para exclusão em lote
        while tasks_to_delete:
            task_to_delete = tasks_to_delete.pop(0)
            deleted_tasks.add(task_to_delete)

            # Encontrar as tarefas filhas
            child_tasks = Task.query.filter_by(task_parent_id=task_to_delete).all()
            tasks_to_delete.extend([child.id for child in child_tasks])

        # Excluir as tarefas em lote
        tasks = Task.query.filter(Task.id.in_(deleted_tasks)).all()
        for task in tasks:
            db.session.delete(task)

        db.session.commit()

        return jsonify(status=200, message="Tarefas e tarefas filhas excluídas com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir tarefas e suas tarefas filhas.", error=str(e))


@task_blueprint.route("/complete_task/<int:task_id>", methods=["PUT"])
@login_required
def complete_task(task_id):
    try:
        child_id = None
        children = current_user.children
        if children:
            child_id = children[0].id

        task = Task.query.get(task_id)

        if not task:
            return jsonify(status=400, message="Tarefa não encontrada.")

        child_task = ChildTask.query.filter_by(child_id=child_id, task_id=task_id).first()

        if not child_task:
            return jsonify(status=400, message="Associação ChildTask não encontrada.")

        child_task.done = 1
        db.session.commit()

        return jsonify(status=200, message="Tarefa marcada como feita com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao marcar tarefa como feita.", error=str(e))
