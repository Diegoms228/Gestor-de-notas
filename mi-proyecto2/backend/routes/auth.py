from flask import Blueprint, request, jsonify, current_app
import bcrypt
import jwt
import datetime
from models.db import get_db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db()
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")
    email = data.get("email", "").strip()
    nombre = data.get("nombre", "").strip()
    apellidos = data.get("apellidos", "").strip()

    # Validación
    if not all([username, password, email, nombre, apellidos]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if len(username) > 50 or len(password) > 100:
        return jsonify({"error": "Datos demasiado largos"}), 400

    # Verificar si usuario o email ya existen
    existente = db.execute(
        "SELECT id FROM usuarios WHERE username = ? OR email = ?",
        (username, email)
    ).fetchone()

    if existente:
        return jsonify({"error": "El usuario o email ya existe"}), 409

    # Hash de la contraseña
    password_hash = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    db.execute(
        "INSERT INTO usuarios (username, email, nombre, apellidos, password_hash) VALUES (?, ?, ?, ?, ?)",
        (username, email, nombre, apellidos, password_hash)
    )
    db.commit()

    return jsonify({"message": "Usuario registrado correctamente"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db()
    data = request.get_json()

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    user = db.execute(
        "SELECT id, username, password_hash FROM usuarios WHERE username = ?",
        (username,)
    ).fetchone()

    # Mismo mensaje si no existe o contraseña incorrecta (evita enumerar usuarios)
    if not user or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "username": user["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token": token, "username": user["username"]}), 200
