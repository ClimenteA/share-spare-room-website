from apps.cda.models.user import UserOnLoginModel
from apps.cda.models.collections import UsersCol, CDACol
from common.password import encrypt
from common.responses import CustomResponse, State
from common.jwt import get_token_for_user_id
from common.logger import log


async def login_user(user: UserOnLoginModel):
    try:
        user = await UsersCol.find_one(
            {"email": user.email, "parola": encrypt(user.parola)},
            projection={"_id": 0, "user_id": 1},
        )
        if not user:
            return CustomResponse(
                content="Emailul sau parola incorecte.",
                status=State.FAILED,
                status_code=400,
            )

        token = await get_token_for_user_id(
            user["user_id"],
            users_col=CDACol.Users,
            blacktoken_col=CDACol.TokenBlackList,
        )

        return CustomResponse(content=token)

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Incearca din nou",
        status=State.FAILED,
        status_code=500,
    )
