from apps.cda.models.collections import UsersCol, ListingsCol
from common.logger import log
from common.responses import CustomResponse, State


async def delete_user(user_id: str):
    try:
        query = {"user_id": user_id}
        await UsersCol.delete_one(query)
        await ListingsCol.delete_many(query)
        return CustomResponse("Utilizatorul a fost sters")
    except Exception as err:
        log.exception(err)
    return CustomResponse(
        content="Incearca din nou",
        status=State.FAILED,
        status_code=500,
    )
