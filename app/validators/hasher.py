import app.database.binder as crud
import passlib.context as crypt


# Hasher settings
myctx = crypt.CryptContext(schemes=["sha256_crypt"])


# Hash password
def encrypt_password(password: str):
    return myctx.hash(password)


# Verify password-email
def check_password(email: str, password: str):
    stored_pass = crud.get_password_hash(email)
    return myctx.verify(password, stored_pass)
