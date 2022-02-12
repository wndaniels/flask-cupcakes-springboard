from flask import Flask, request, jsonify, render_template
from itsdangerous import json
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yupp1234'

connect_db(app)

"""Flask app for Cupcakes"""


@app.route('/')
def list_cupcakes_html():
    """ Render homepage where all cupcakes will be shown in a list via HTML, and a form to add new cupcakes will be shown. """
    return render_template('index.html')


@app.route('/api/cupcakes')
def list_cupcakes():
    """ Show full API list of all cupcakes """
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    """ Handle POST request to add new cupcake to the API"""
    new_cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"],
                          rating=request.json["rating"], image=request.json["image"])

    db.session.add(new_cupcake)
    db.session.commit()

    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """ Show API details of selected cupcake by id """
    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def edit_cupcake(id):
    """ Handle PATCH request to update/edit cupcake details within the API """
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """ Handle DELETE request to delete cupcake from the API """
    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")
