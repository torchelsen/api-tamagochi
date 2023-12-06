from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Item, db
import base64
from io import BytesIO

item_blueprint = Blueprint("item", __name__, url_prefix="/item")

def init_app(app):
    # Your initialization logic here
    app.register_blueprint(item_blueprint)


@item_blueprint.route("/create_item", methods=["POST"])
@login_required
def create_item():
    name = request.form.get("name")
    item_type = request.form.get("type")
    description = request.form.get("description")
    image = request.files.get("image")
    price = request.form.get("price")
    
    if not all([name, item_type, description, image, price]):
        return jsonify(status=400, message="Item inválido ou dados faltando."), 400

    new_item = Item(
        name=name,
        type=item_type,
        description=description,
        image=image.read(),
        price=float(price)
    )

    db.session.add(new_item)
    db.session.commit()

    return jsonify(status=200, message="Item criado com sucesso.")

@item_blueprint.route("/get_item/<int:item_id>", methods=["GET"])
@login_required
def get_item(item_id):
    try:
        item = Item.query.get(item_id)
        
        if not item:
            return jsonify(status=404, message="Item não encontrado.")
        
        if item.image:
            buffered = BytesIO(item.image)
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
        else:
            encoded_image = None

        item_data = {
            "id": item.id,
            "name": item.name,
            "type": item.type,
            "description": item.description,
            "price": item.price,
            "image": encoded_image
        }

        # Decodifica a imagem e salva localmente, feita para testes
        image_bytes = base64.b64decode(encoded_image)
        with open('imagem2.png', "wb") as file:
            file.write(image_bytes)

        return jsonify(status=200, task=item_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter tarefa.", error=str(e))

@item_blueprint.route("/get_all_items", methods=["GET"])
@login_required
def get_all_items():
    try:
        items = Item.query.all()

        items_data = []
        for item in items:
            if item.image:
                buffered = BytesIO(item.image)
                encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            else:
                encoded_image = None

            item_data = {
                "id": item.id,
                "name": item.name,
                "type": item.type,
                "description": item.description,
                "price": item.price,
                "image": encoded_image
            }

            items_data.append(item_data)

        
        return jsonify(status=200, items=items_data)

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao obter itens.", error=str(e))


@item_blueprint.route("/update_item/<int:item_id>", methods=["PUT"])
@login_required
def update_item(item_id):
    try:
        if request.content_type.startswith('multipart/form-data'):
            item = Item.query.get(item_id)

            if not item:
                return jsonify(status=404, message="Item não encontrado.")

            item.name = request.form.get("name", item.name)
            item.type = request.form.get("type", item.type)
            item.description = request.form.get("description", item.description)
            item.price = float(request.form.get("price", item.price))

            image = request.files.get("image")
            if image:
                item.image = image.read()

            db.session.commit()

            return jsonify(status=200, message="Item atualizado com sucesso.")

        elif request.is_json:
            data = request.get_json()
            item = Item.query.get(item_id)

            if not item:
                return jsonify(status=404, message="Item não encontrado.")

            item.name = data.get("name", item.name)
            item.type = data.get("type", item.type)
            item.description = data.get("description", item.description)
            item.price = float(data.get("price", item.price))

            if 'image' in data:
                item.image = data['image'].encode()

            db.session.commit()

            return jsonify(status=200, message="Item atualizado com sucesso.")

        else:
            return jsonify(status=400, message="Tipo de conteúdo não suportado.")

    except Exception as e:
        return jsonify(status=500, message="Erro interno ao atualizar item.", error=str(e))

@item_blueprint.route("/delete_item/<int:item_id>", methods=["DELETE"])
@login_required
def delete_item(item_id):
    try:
        item = Item.query.get(item_id)

        if not item:
            return jsonify(status=404, message="Item não encontrado.")

        db.session.delete(item)
        db.session.commit()

        return jsonify(status=200, message="Item excluído com sucesso.")
    except Exception as e:
        return jsonify(status=500, message="Erro interno ao excluir item.", error=str(e))

