from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jprogramtech:test@localhost/karmic'

db = SQLAlchemy(app)
CORS(app)
ma = Marshmallow(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(120), unique=True)
    price = db.Column(db.Integer)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    def __repr__(self):
        return '<Item %r>' % self.name


class ItemSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'description', 'price')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True);


########## API ############

# create item
@app.route('/item', methods=['POST'])
def add_item():
    item = Item(request.json['name'], request.json['description'], request.json['price'])
    db.session.add(item)
    db.session.commit()
    result = item_schema.dump(Item.query.get(item.id))
    return jsonify(result.data)

# get all itmes
@app.route('/item', methods=['GET'])
def get_items():
    items = Item.query.all()
    result = items_schema.dump(items)
    return items_schema.jsonify(result.data)

# get item by id
@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    return item_schema.jsonify(item)


# delete item by id
@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return item_schema.jsonify(item)


if __name__ == "__main__":
    app.run()
