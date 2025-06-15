from flask_smorest import Blueprint
from flask import request
from app.api.schemas import ChatSchema
from app.services.llm import generate_response

blp = Blueprint("chat", "chat", url_prefix="/", description="LLM Chat API")

@blp.route("/ping")
def ping():
    return {"message": "Jarvish is online 🚀"}

@blp.route("/chat", methods=["POST"])
@blp.arguments(ChatSchema)
def chat(data):
    prompt = data["prompt"]
    reply = generate_response(prompt)
    return {"response": reply}
