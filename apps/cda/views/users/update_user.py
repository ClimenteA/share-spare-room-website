from apps.cda.models.user import UserOnUpdateModel
from apps.cda.models.collections import UsersCol
from common.logger import log
from common.responses import CustomResponse, State


async def update_user(user_id: str, user: UserOnUpdateModel):
    try:
        updated = await UsersCol.update_one(
            {"user_id": user_id}, data=user.model_dump()
        )
        if updated:
            return CustomResponse(content="Datele au fost actualizate")
    except Exception as err:
        log.exception(err)
        return CustomResponse(
            content="Verifica daca datele corespund cerintelor",
            status=State.FAILED,
            status_code=400,
        )
