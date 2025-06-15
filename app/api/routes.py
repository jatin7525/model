from flask_smorest import Blueprint
from flask import request, jsonify, send_file, after_this_request

from app.services.chat_model import generate_response
from app.services.img_gen_model import generate_image
from app.api.schemas import ChatInputSchema, ImageInputSchema
from app.utils.route import check_passcode
from app.utils.logger import log_info, log_error

blp = Blueprint("chat", "chat", url_prefix="/", description="LLM Chat API")


@blp.route("/ping", methods=["GET"])
def ping():
    log_info("Ping request received")
    if request.method == "GET":
        log_info("Ping successful")
    else:
        log_error("Ping failed - unsupported method")
    return {"message": "Jarvish is online 🚀"}


@blp.route("/chat", methods=["POST"])
@blp.arguments(ChatInputSchema)
def chat(data):
    if not check_passcode(data):
        log_error("Unauthorized access attempt")
        return jsonify({"error": "Unauthorized"}), 401

    prompt = data["prompt"]
    reply = generate_response(prompt)
    log_info(f"Generated response for prompt: {prompt}")
    if not reply:
        log_error("Failed to generate response")
        return jsonify({"error": "Failed to generate response"}), 500
    log_info(f"Response length: {len(reply)} characters")
    log_info(f"Response: {reply}...")
    return {"response": reply}


@blp.route("/image", methods=["POST"])
@blp.arguments(ImageInputSchema)
def generate_image_route(data):
    if not check_passcode(data):
        log_error("Unauthorized access attempt")
        return jsonify({"error": "Unauthorized"}), 401

    prompt = data.get("prompt", "A cute robot drawing a cat").strip()
    if not prompt:
        log_error("Prompt for image generation is empty")
        return jsonify({"error": "Prompt is empty"}), 400

    try:
        log_info(f"Generating image for prompt: {prompt}")
        output_path = generate_image(prompt)

        if not output_path or not os.path.exists(output_path):
            raise FileNotFoundError("Image generation failed or file missing")

        log_info(f"Image ready at: {output_path}")

        @after_this_request
        def delete_temp(response):
            try:
                os.remove(output_path)
                log_info(f"Deleted temporary image: {output_path}")
            except Exception as e:
                log_error(f"Error deleting file {output_path}: {e}")
            return response

        return send_file(output_path, mimetype="image/png", as_attachment=True, download_name="image.png")

    except Exception as e:
        log_error(f"Failed to generate image: {e}")
        return jsonify({"error": "Failed to generate image"}), 500
