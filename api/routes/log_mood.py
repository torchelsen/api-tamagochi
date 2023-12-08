from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Mood, LogMood, Child, ChildTask, db
from datetime import datetime

log_mood_blueprint = Blueprint("log_mood", __name__, url_prefix="/log_mood")
def init_app(app):
    # Your initialization logic here
    app.register_blueprint(log_mood_blueprint)


@log_mood_blueprint.route("/add_log_mood", methods=["POST"])
@login_required
def add_log_mood():
    data = request.get_json()
    
    now = datetime.now()

    required_fields = ["mood_id", "child_id", "child_task_id"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(status=400, message="LogMood inválido ou dados faltando."), 400

    mood = Mood.query.get(data["mood_id"])

    if not mood:
        return jsonify(status=404, message="Mood não encontrado.")

    child_id = data["child_id"]
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()

    if not child:
        return jsonify(status=404, message="Criança não encontrada.")
    
    child_task = ChildTask.query.get(data["child_task_id"])

    if not child_task:
        return jsonify(status=404, message="Esta tarefa não está associada a esta criança.")
    
    new_log_mood = LogMood(
        mood_id=data["mood_id"],
        child_id=data["child_id"],
        child_task_id=data["child_task_id"],
        timestamp=now
    )

    db.session.add(new_log_mood)
    db.session.commit()

    return jsonify(status=200, message="Log criado com sucesso.")

@log_mood_blueprint.route("/get_log_mood/<int:log_mood_id>", methods=["GET"])
@login_required
def get_log_mood(log_mood_id):
    try:
        log_mood = LogMood.query.get(log_mood_id)

        if not log_mood:
            return jsonify(status=404, message="Log não encontrado.")

        log_mood_data = {
            "id": log_mood.id,
            "mood_id": log_mood.mood_id,
            "child_id": log_mood.child_id,
            "child_task_id": log_mood.child_task_id,
            "timestamp": log_mood.timestamp,
        }

        return jsonify(status=200, log_mood=log_mood_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter Log.", error=str(e))
    
@log_mood_blueprint.route("/get_all_log_moods", methods=["GET"])
@login_required
def get_all_log_moods():
    try:
        all_log_moods = LogMood.query.all()

        log_mood_data = [{
            "id": log_mood.id,
            "mood_id": log_mood.mood_id,
            "child_id": log_mood.child_id,
            "child_task_id": log_mood.child_task_id,
            "timestamp": log_mood.timestamp,
        } for log_mood in all_log_moods]

        return jsonify(status=200, log_moods=log_mood_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todas os Logs.", error=str(e))

@log_mood_blueprint.route("/update_log_mood/<int:log_mood_id>", methods=["PUT"])
@login_required
def update_log_mood(log_mood_id):
    try:
        data = request.get_json()

        now = datetime.now()

        if not data:
            return jsonify(status=400, message="Dados inválidos.")

        log_mood = LogMood.query.get(log_mood_id)

        if not log_mood:
            return jsonify(status=404, message="Log não encontrado.")

        mood_id = data["mood_id"]
        mood = Mood.query.get(mood_id)

        if not mood:
            return jsonify(status=404, message="mood não encontrado.")

        child_id = data["child_id"]
        child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()

        if not child:
            return jsonify(status=404, message="Criança não encontrada.")
        
        child_task = ChildTask.query.get(data["child_task_id"])

        if not child_task:
            return jsonify(status=404, message="Esta tarefa não está associada a esta criança.")

        log_mood.mood_id = data.get("mood_id", log_mood.mood_id)
        log_mood.child_id = data.get("child_id", log_mood.child_id)
        log_mood.child_task_id = data.get("child_task_id", log_mood.child_task_id)
        log_mood.timestamp = now
        
        db.session.commit()

        return jsonify(status=200, message="Log atualizado com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar Log.", error=str(e))

@log_mood_blueprint.route("/delete_log_mood/<int:log_mood_id>", methods=["DELETE"])
@login_required
def delete_log_mood(log_mood_id):
    try:
        log_mood = LogMood.query.get(log_mood_id)

        if not log_mood:
            return jsonify(status=404, message="Log não encontrado.")

        db.session.delete(log_mood)
        db.session.commit()

        return jsonify(status=200, message="Log excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir Log.", error=str(e))