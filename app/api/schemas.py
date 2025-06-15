# Just a utility for structuring
def format_chat(prompt: str):
    return {
        "prompt": prompt.strip(),
        "tokens": len(prompt.split())
    }
