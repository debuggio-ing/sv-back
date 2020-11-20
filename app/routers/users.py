from fastapi import APIRouter, UploadFile, File, Response, status

from app.database.binder import *
from app.validators.auth_validator import *
from app.validators.game_validator import *
from app.validators.hasher import *

# Users endpoints' router
r = users_router = APIRouter()


# Create new user.
@r.post("/register/",
        status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserReg) -> int:
    id = register_user(user=new_user)
    if id == -1:
        raise HTTPException(status_code=409, detail="Email already in use")

    return id


# Return user information.
@r.get("/users/info/", response_model=UserPublic)
def get_user(auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)

    return get_user_public(user_email=user_email)


# Receives an img from the user
@r.post("/users/picture/")
def create_upload_file(
        file: UploadFile = File(...),
        auth: AuthJWT = Depends()):
    contents = file.file.read()
    user_email = validate_user(auth=auth)
    # AGREGAR CHEQUEOS PARA VALIDAR IMAGEN
    set_picture(user_email=user_email, image=contents)
    return 1


# Returns the profile picture of a user
@r.get("/users/picture/")
def get_profile_picture(auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)
    picture = get_picture(user_email=user_email)
    return Response(content=picture)


# Return user information.
@r.post("/users/info/modify/", response_model=UserPublic)
def modify_user_info(new_profile: UserProfile, auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)
    # Needs to check the values inserted are appropriate
    set_nickname(user_email=user_email, nickname=new_profile.nickname)
    if new_profile.password != '' and check_password(user_email, new_profile.oldpassword):
        set_password(user_email=user_email, password=new_profile.password)
    else:
        raise HTTPException(status_code=401, detail='Bad password')
    return get_user_public(user_email=user_email)


# Return all lobbies that user with jwt is in.
@r.get("/users/games/", response_model=UserGames)
def get_user_active_games(auth: AuthJWT = Depends()):
    user_email = validate_user(auth=auth)
    games = get_active_games(user_email)

    return UserGames(email=user_email, games=games)


# Send email to recover account.
@r.post("/recover/")
def recover_user(email: RecoverAccount):
    return 1


# Verify email.
@r.post("/verify/", status_code=200)
def verify_email(user_email: str, input_code: int) -> bool:
    code = get_verification_code(user_email=user_email)

    if code != input_code:
        raise HTTPException(status_code=409, detail="Invalid code.")

    set_user_email_verified(user_email=user_email)

    return UserVerify(email=user_email, verified=True)
