import uuid
import os
from diffusers import StableDiffusionPipeline
import torch
from app.core.constants import IMG_PATH, IMAGE_MODEL_ID
from app.utils.logger import log_info, log_error

# Load the model
pipe = StableDiffusionPipeline.from_pretrained(
    IMAGE_MODEL_ID,
    torch_dtype=torch.float16
)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt: str) -> str:
    # === Basic prompt checks ===
    if not isinstance(prompt, str) or not prompt.strip():
        log_error("Invalid prompt: Must be a non-empty string")
        return None
    if len(prompt) > 512:
        log_error("Prompt too long (max 512 characters)")
        return None

    # === Create filename & path ===
    filename = f"{uuid.uuid4().hex[:8]}.png"
    output_path = os.path.join(IMG_PATH, filename)
    log_info(f"Generating image for prompt: {prompt}")
    log_info(f"Output will be saved to: {output_path}")

    # === Ensure image directory exists and is writable ===
    try:
        os.makedirs(IMG_PATH, exist_ok=True)
    except Exception as e:
        log_error(f"Failed to create image directory {IMG_PATH}: {e}")
        return None

    if not os.access(IMG_PATH, os.W_OK):
        log_error(f"Directory not writable: {IMG_PATH}")
        return None

    # === Generate the image ===
    try:
        result = pipe(prompt)
        image = result.images[0]
        if image is None or not hasattr(image, 'save'):
            log_error("Generated image is invalid or missing 'save' method")
            return None
        image.save(output_path)
    except Exception as e:
        log_error(f"Image generation failed: {e}")
        return None

    # === Post-generation validation ===
    if not os.path.isfile(output_path):
        log_error(f"Generated file does not exist: {output_path}")
        return None
    if not os.access(output_path, os.R_OK):
        log_error(f"File is not readable: {output_path}")
        return None

    log_info(f"Image successfully generated and saved at: {output_path}")
    return output_path
