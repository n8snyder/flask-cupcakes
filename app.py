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


@app.get("/api/cupcakes")
def list_cupcakes():
    """Return JSON of all cupcakes."""

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return (jsonify(cupcakes=cupcakes), 200)


@app.get("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Return details of a single cupcake."""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)


@app.post("/api/cupcakes")
def create_cupcake():
    """Create a new cupcake in the DB."""

    cupcake = request.json
    print(cupcake)
    new_cupcake = Cupcake(**cupcake)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)
