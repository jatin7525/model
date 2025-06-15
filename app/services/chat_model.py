from transformers import AutoTokenizer, AutoModelForCausalLM
from app.utils.logger import log_info, log_error
from app.core.constants import CHAT_MODEL_NAME
import torch

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(CHAT_MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load model on CPU and use float32 (important for CPU usage)
model = AutoModelForCausalLM.from_pretrained(
    CHAT_MODEL_NAME,
    torch_dtype=torch.float32
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_response(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

    log_info(f"Tokenized input length: {inputs['input_ids'].shape[1]}")

    if inputs["input_ids"].shape[1] > 2048:
        log_error("Input prompt exceeds maximum length of 2048 tokens")
        return "Error: Input prompt is too long."

    try:
        outputs = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            pad_token_id=tokenizer.pad_token_id,
            max_new_tokens=100,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.8,
            repetition_penalty=1.2
        )
    except Exception as e:
        log_error(f"Model generation failed: {e}")
        return "Error: Model generation failed."

    if outputs is None or outputs.shape[0] == 0:
        log_error("Model did not return any output")
        return "Error: Failed to generate response."

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    log_info("Response generation successful")
    log_info(f"Response: {response}")
    return response
