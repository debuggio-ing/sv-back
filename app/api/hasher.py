
import app.database.crud as crud
import passlib.context as crypt


#configurar el hash
myctx = crypt.CryptContext(schemes=["sha256_crypt"])

#Hashear una pass
def encrypt_password(password: str):

    return myctx.hash(password)

#hashear y verificar si coincide con la bd
def check_password(email: str, password: str):

    #seleccionar el jugador con pass y contraseña
    hashed_pass = encrypt_password(password)

    stored_pass = crud.get_password_hash(email)

    return myctx.verify(hashed_pass, stored_pass)