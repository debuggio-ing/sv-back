from fastapi import FastAPI, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, Field

# Source:
# https://pypi.org/project/fastapi-jwt-auth/

# It is necessary to set AUTHJWT_SECRET_KEY environment variable
# export AUTHJWT_SECRET_KEY=secretkey

app = FastAPI()

class User(BaseModel):
    username: str = Field(...,min_length=1)
    password: str = Field(...,min_length=1)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.post('/login',status_code=200)
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != 'test' or user.password != 'test':
        raise HTTPException(status_code=401,detail='Bad username or password')

    # identity must be between string or integer
    access_token = Authorize.create_access_token(identity=user.username)
    return {"access_token": access_token}

@app.get('/protected',status_code=200)
def protected(Authorize: AuthJWT = Depends()):
    # Protect an endpoint with jwt_required, which requires a valid access token
    # in the request to access.
    Authorize.jwt_required()

    # Access the identity of the current user with get_jwt_identity
    current_user = Authorize.get_jwt_identity()
    return {"logged_in_as": current_user}
