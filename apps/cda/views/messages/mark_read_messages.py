import apps.cda.models.collections as c
from common.responses import CustomResponse, State
from common.logger import log


async def mark_read_messages(user_id: str, message_ids: list[str]):
    try:
        poster = await c.MessagesCol.count(
            {"poster_user_id": user_id, "message_id": {"$in": message_ids}}
        )
        if poster:
            updated = await c.MessagesCol.update_many(
                filters={
                    "poster_user_id": user_id,
                    "message_id": {"$in": message_ids},
                },
                data={"poster_seen_it": True},
            )
            if updated:
                return CustomResponse(
                    content="Mesajele au fost marcate ca citite (Poster)"
                )

        interested = await c.MessagesCol.count(
            {"interested_user_id": user_id, "message_id": {"$in": message_ids}}
        )
        if interested:
            updated = await c.MessagesCol.update_many(
                filters={
                    "interested_user_id": user_id,
                    "message_id": {"$in": message_ids},
                },
                data={"interested_seen_it": True},
            )
            if updated:
                return CustomResponse(
                    content="Mesajele au fost marcate ca citite (Intersted)"
                )
    except Exception as err:
        log.exception(err)
    return CustomResponse(
        content="Incearca din nou",
        status=State.FAILED,
        status_code=500,
    )
