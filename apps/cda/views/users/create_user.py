from datetime import datetime
from apps.cda.models.user import UserOnRegisterModel, UserOnDbModel
from common.responses import CustomResponse, State
from common.logger import log
from apps.cda.models.collections import UsersCol
from common.validators import get_encrypted_password, get_lower_email


async def create_user(user: UserOnRegisterModel):
    try:
        user.email = get_lower_email(user.email)
        user.parola = get_encrypted_password(user.parola)

        already_exists = await UsersCol.count({"email": user.email})
        if already_exists:
            return CustomResponse(
                content="Emailul este deja inregistrat.",
                status=State.FAILED,
                status_code=400,
            )

        newuser = UserOnDbModel(
            email=user.email,
            parola=user.parola,
            nume=user.email.split("@")[0],
            created_at=datetime.utcnow().isoformat(),
        )

        inserted = await UsersCol.insert_one(newuser.model_dump())

        if inserted:
            return CustomResponse(content="Contul a fost creat!")

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Emailul sau parola nu corespund cerintelor",
        status=State.FAILED,
        status_code=400,
    )
