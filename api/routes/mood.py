from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Mood, db
import base64
from io import BytesIO


mood_blueprint = Blueprint("mood", __name__, url_prefix="/mood")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(mood_blueprint)


@mood_blueprint.route("/add_mood", methods=["POST"])
@login_required
def add_mood():
    name = request.form.get("name")
    category = request.form.get("category")
    image = request.files.get("image")

    if not all([name, category, image]):
        return jsonify(status=400, message="Item inválido ou dados faltando."), 400

    new_mood = Mood(
        name=name,
        category=category,
        image=image.read(),
    )

    db.session.add(new_mood)
    db.session.commit()

    return jsonify(status=200, message="Mood criado com sucesso.")

@mood_blueprint.route("/get_mood/<int:mood_id>", methods=["GET"])
@login_required
def get_mood(mood_id):
    try:
        mood = Mood.query.get(mood_id)
        
        if not mood:
            return jsonify(status=404, message="TaskReward não encontrado.")
        

        buffered = BytesIO(mood.image)
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        mood_data = {
            "id": mood.id,
            "name": mood.name,
            "category": mood.category,
            "image": encoded_image
        }

        return jsonify(status=200, mood=mood_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter mood.", error=str(e))

@mood_blueprint.route("/get_all_moods", methods=["GET"])
@login_required
def get_all_moods():
    try:
        all_moods = Mood.query.all()

        moods_data = []

        for mood in all_moods:
            buffered = BytesIO(mood.image)
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            mood_data = {
                "id": mood.id,
                "name": mood.name,
                "category": mood.category,
                "image": encoded_image
            }
            moods_data.append(mood_data)

        return jsonify(status=200, mood=moods_data)
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter todos os moods.", error=str(e))


@mood_blueprint.route("/update_mood/<int:mood_id>", methods=["PUT"])
@login_required
def update_mood(mood_id):
    try:
        if request.content_type.startswith('multipart/form-data'):
            mood = Mood.query.get(mood_id)

            if not mood:
                return jsonify(status=404, message="mood não encontrado.")

            mood.name = request.form.get("name", mood.name)
            mood.category = request.form.get("category", mood.category)
            image = request.files.get("image")
            if image:
                mood.image = image.read()

            db.session.commit()

            return jsonify(status=200, message="Mood atualizado com sucesso.")

        elif request.is_json:
            data = request.get_json()
            mood = mood.query.get(mood_id)

            if not mood:
                return jsonify(status=404, message="mood não encontrado.")

            mood.name = data.get("name", mood.name)
            mood.type = data.get("type", mood.type)
            mood.description = data.get("description", mood.description)
            mood.price = float(data.get("price", mood.price))

            if 'image' in data:
                mood.image = data['image'].encode()

            db.session.commit()

            return jsonify(status=200, message="mood atualizado com sucesso.")

        else:
            return jsonify(status=400, message="Tipo de conteúdo não suportado.")

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar mood.", error=str(e))

@mood_blueprint.route("/delete_mood/<int:mood_id>", methods=["DELETE"])
@login_required
def delete_mood(mood_id):
    try:
        mood = Mood.query.get(mood_id)

        if not mood:
            return jsonify(status=404, message="Mood não encontrado.")
        
        db.session.delete(mood)
        db.session.commit()

        return jsonify(status=200, message="Mood excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir mood.", error=str(e))

