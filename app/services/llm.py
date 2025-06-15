from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "tiiuae/falcon-rw-1b"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(inputs["input_ids"], max_new_tokens=100)
    return tokenizer.decode(output[0], skip_special_tokens=True)
