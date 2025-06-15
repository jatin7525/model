from app.core.constants import SECRET_PASSCODE

def check_passcode(data):
    passcode = data["passcode"] if "passcode" in data else None
    if not passcode:
        return False
    if len(passcode) != 6 or not passcode.isdigit():
        return False
    return passcode == SECRET_PASSCODE