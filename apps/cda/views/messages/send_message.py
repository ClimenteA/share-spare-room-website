from apps.cda.models.message import MessageOnCreateModel, MessageOnDbModel
from common.logger import log
from common.responses import CustomResponse, State
from apps.cda.models.collections import (
    ListingsCol,
    MessagesCol,
    BlockCol,
)


async def send_message(sender_user_id: str, message: MessageOnCreateModel):
    try:
        if sender_user_id == message.to_user_id:
            return CustomResponse(
                content="Nu iti poti trimite singur mesaje la anuntul postat",
                status=State.FAILED,
                status_code=400,
            )

        listing_owner = await ListingsCol.find_one({"listing_id": message.listing_id})
        if not listing_owner:
            return CustomResponse(
                content="Anuntul nu exista",
                status=State.FAILED,
                status_code=400,
            )

        query = {"user_id": sender_user_id, "listing_id": message.listing_id}
        sender_is_poster = await ListingsCol.find_one(query)

        current_nbr_of_messages = await MessagesCol.count({})
        if current_nbr_of_messages > 500:
            older_messages = await MessagesCol.find_many(
                {}, limit=250, sort=[("updated_at", 1)], projection={"_id": 1}
            )
            older_messages_ids = [m["_id"] for m in older_messages]
            await MessagesCol.delete_many({"_id": {"$in": older_messages_ids}})

        if sender_is_poster:
            msg = MessageOnDbModel(
                poster_user_id=sender_user_id,
                interested_user_id=message.to_user_id,
                listing_id=message.listing_id,
                poster_message=message.message,
                interested_message=None,
                poster_seen_it=True,
            )
            updated = await MessagesCol.insert_one(msg.model_dump())
            if updated:
                return CustomResponse(content="Mesajul a fost trimis")
            raise Exception("Can't update")
        else:
            blocked_user = await BlockCol.count(
                {
                    "blocked_by_user_id": listing_owner["user_id"],
                    "blocked_user_id": sender_user_id,
                }
            )
            if blocked_user:
                return CustomResponse(
                    content="Nu mai poti trimite mesaje acestui utilizator.",
                    status=State.FAILED,
                    status_code=400,
                )

            msg = MessageOnDbModel(
                poster_user_id=message.to_user_id,
                interested_user_id=sender_user_id,
                listing_id=message.listing_id,
                poster_message=None,
                interested_message=message.message,
                interested_seen_it=True,
            )
            updated = await MessagesCol.insert_one(msg.model_dump())
            if updated:
                return CustomResponse(content="Mesajul a fost trimis")
            raise Exception("Can't update")

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Incearca din nou", status=State.FAILED, status_code=500
    )
