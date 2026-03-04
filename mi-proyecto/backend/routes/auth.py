from flask import Blueprint, request, jsonify, current_app
import bcrypt
import jwt
import sqlite3
from models.db import get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db()
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # Validación básica
    if not username or not password:
        return jsonify({"error": "Datos inválidos"}), 400

    if len(username) > 50 or len(password) > 100:
        return jsonify({"error": "Datos demasiado largos"}), 400

    # Verificar si usuario existe
    user = db.execute(
        "SELECT id FROM usuarios WHERE username = ?",
        (username,)
    ).fetchone()

    if user:
        return jsonify({"error": "Usuario ya existe"}), 409

    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    # Insertar usuario
    db.execute(
        "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )

    db.commit()

    return jsonify({"message": "Usuario registrado"}), 201