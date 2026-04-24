import os
from flask import Flask, jsonify
from flask_cors import CORS
from models.db import init_db
from routes.auth import auth_bp
from routes.notes import notes_bp

app = Flask(__name__)
CORS(app)

# SECRET_KEY leída de variable de entorno (nunca hardcodeada)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cambia_esto_en_produccion")

init_db(app)

app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(notes_bp, url_prefix="/api")

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Error interno"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
