from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException


# Checks if the user is properly validated and returns its email or raises
# an exception
def validate_user(auth: AuthJWT = Depends()):
    # check if token is valid
    auth.jwt_required()

    # get user's email
    user_email = auth.get_jwt_identity()
    if user_email is None:
        raise HTTPException(status_code=409, detail='Corrupted JWT')
    return user_email
