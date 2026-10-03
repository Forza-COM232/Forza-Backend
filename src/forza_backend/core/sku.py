import secrets
import string

def generate_sku(prefix: str = "SMS") -> str:
    suffix = "".join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(8)
    )
    
    return f"{prefix}-{suffix}"