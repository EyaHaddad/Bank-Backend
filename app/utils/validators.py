import re

def validate_password(password: str) -> bool:
    return (
        len(password) >= 12 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*()]", password)
    )
