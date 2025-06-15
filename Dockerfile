FROM python:3.10-slim

ARG HUGGINGFACE_TOKEN

WORKDIR /app

ENV HF_HOME=/tmp/hf-cache
ENV HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN

# Install basic dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

RUN pip install torch transformers diffusers
RUN pip install gunicorn
RUN pip install prettyprinter  

# Copy source code
COPY ./app app
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Runtime: download models + run Flask
CMD bash -c "\
    echo '🔑 Logging into HuggingFace' && \
    pip install --no-cache-dir huggingface_hub && \
    huggingface-cli login --token $HUGGINGFACE_TOKEN && \
    echo 'Downloading models...' && \
    python -c \"from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('stabilityai/sd-turbo')\" && \
    python -c \"from transformers import AutoTokenizer, AutoModelForCausalLM; model_name='TinyLlama/TinyLlama-1.1B-Chat-v1.0'; AutoTokenizer.from_pretrained(model_name); AutoModelForCausalLM.from_pretrained(model_name)\" && \
    echo 'Starting Flask app' && \
    gunicorn  pp.main:app --bind 0.0.0.0:8000 --timeout 120 \
"
