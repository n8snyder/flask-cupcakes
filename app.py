"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "THIS DOESNT MATTER"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.debug = True


toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.get("/")
def homepage():
    """Homepage, displays create cupcake form and list of cupcakes."""

    return render_template("cupcakes.html")


@app.get("/api/cupcakes")
def list_cupcakes():
    """Return JSON of all cupcakes.

    {cupcakes: [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.get("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Return details of a single cupcake.

    {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post("/api/cupcakes")
def create_cupcake():
    """Create a new cupcake in the DB. Return JSON of the new cupcake:

    {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = request.json
    new_cupcake = Cupcake(
        flavor=cupcake["flavor"],
        size=cupcake["size"],
        rating=cupcake["rating"],
        image=cupcake["image"],
    )

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)


@app.patch("/api/cupcakes/<int:id>")
def update_cupcake(id):
    """Updates a cupcake, not all fields are required. Return JSON of updated
    cupcake:

    {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(id)
    cupcake_updates = request.json

    cupcake.flavor = cupcake_updates.get("flavor", cupcake.flavor)
    cupcake.size = cupcake_updates.get("size", cupcake.size)
    cupcake.rating = cupcake_updates.get("rating", cupcake.rating)
    cupcake.image = cupcake_updates.get("image", cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.delete("/api/cupcakes/<int:id>")
def delete_cupcake(id):
    """Delete a cupcake. Return JSON with ID of deleted cupcake.

    {deleted: [cupcake-id]}
    """

    cupcake = Cupcake.query.get_or_404(id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(deleted=cupcake.id)
