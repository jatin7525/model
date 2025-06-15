from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data.get("username") == "jatin" and data.get("password") == "1234":
        token = create_access_token(identity="jatin")
        return jsonify(access_token=token)
    return jsonify({"msg": "Invalid credentials"}), 401

@auth_bp.route("/secure-ping", methods=["GET"])
@jwt_required()
def secure_ping():
    user = get_jwt_identity()
    return jsonify({"message": f"Hello {user}, secure ping 🔒"})
