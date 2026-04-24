from flask import Blueprint, request, jsonify
from models.db import get_db
from middleware.auth_middleware import token_required

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/notas", methods=["GET"])
@token_required
def get_notas(token_data):
    db = get_db()
    notas = db.execute(
        "SELECT id, titulo, contenido, created_at, updated_at FROM notas WHERE user_id = ? ORDER BY updated_at DESC",
        (token_data["user_id"],)
    ).fetchall()
    return jsonify([dict(n) for n in notas]), 200


@notes_bp.route("/notas", methods=["POST"])
@token_required
def create_nota(token_data):
    db = get_db()
    data = request.get_json()

    titulo = data.get("titulo", "").strip()
    contenido = data.get("contenido", "").strip()

    if not titulo or not contenido:
        return jsonify({"error": "Título y contenido son obligatorios"}), 400

    cursor = db.execute(
        "INSERT INTO notas (user_id, titulo, contenido) VALUES (?, ?, ?)",
        (token_data["user_id"], titulo, contenido)
    )
    db.commit()

    return jsonify({"message": "Nota creada", "id": cursor.lastrowid}), 201


@notes_bp.route("/notas/<int:nota_id>", methods=["PUT"])
@token_required
def update_nota(token_data, nota_id):
    db = get_db()
    data = request.get_json()

    titulo = data.get("titulo", "").strip()
    contenido = data.get("contenido", "").strip()

    if not titulo or not contenido:
        return jsonify({"error": "Título y contenido son obligatorios"}), 400

    result = db.execute(
        """UPDATE notas SET titulo = ?, contenido = ?, updated_at = CURRENT_TIMESTAMP
           WHERE id = ? AND user_id = ?""",
        (titulo, contenido, nota_id, token_data["user_id"])
    )
    db.commit()

    if result.rowcount == 0:
        return jsonify({"error": "Nota no encontrada"}), 404

    return jsonify({"message": "Nota actualizada"}), 200


@notes_bp.route("/notas/<int:nota_id>", methods=["DELETE"])
@token_required
def delete_nota(token_data, nota_id):
    db = get_db()

    result = db.execute(
        "DELETE FROM notas WHERE id = ? AND user_id = ?",
        (nota_id, token_data["user_id"])
    )
    db.commit()

    if result.rowcount == 0:
        return jsonify({"error": "Nota no encontrada"}), 404

    return jsonify({"message": "Nota eliminada"}), 200
