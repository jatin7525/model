import os
from app import create_app
os.environ["HF_HOME"] = "/app/.cache"

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)
