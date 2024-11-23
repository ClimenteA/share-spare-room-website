import apps.cda.models.collections as c
from common.responses import CustomResponse, State
from common.logger import log


async def delete_messages(user_id: str, message_ids: list[str]):
    try:
        deleted = await c.MessagesCol.delete_many(
            {
                "message_id": {"$in": message_ids},
                "$or": [
                    {"poster_user_id": user_id},
                    {"interested_user_id": user_id},
                ],
            }
        )
        if deleted:
            return CustomResponse(content="Mesajele au fost sterse")
    except Exception as err:
        log.exception(err)
    return CustomResponse(
        content="Incearca din nou",
        status=State.FAILED,
        status_code=500,
    )
