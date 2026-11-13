from klj_site.database.DbConnection import DbConnection
from klj_site.services.extra import get_user_id
import hashlib
import hmac
import secrets


def hash_password(plain_password: str) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a 16-byte random salt."""
    salt = secrets.token_bytes(16)
    iterations = 600_000
    dk = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
    return f"{iterations}:{salt.hex()}:{dk.hex()}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verifies a plaintext password against the stored 'iterations:salt:hash' string."""
    try:
        iterations_str, salt_hex, hash_hex = stored_hash.split(":")
        dk = hashlib.pbkdf2_hmac(
            "sha256",
            plain_password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations_str),
        )
        return hmac.compare_digest(dk.hex(), hash_hex)
    except ValueError:
        return False


def is_valid_user(username, password) -> bool:
    db = DbConnection()
    user_id: int | None = get_user_id(username)
    if not user_id: return False

    if verify_password(password, db.get_password_hash(user_id)):
        return True
    return False
