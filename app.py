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
    return jsonify(cupcakes)
