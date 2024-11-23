import apps.cda.models.collections as c
from common.responses import CustomResponse, State
from common.logger import log


async def get_messages(user_id: str, listing_id: str):
    try:
        messages = await c.MessagesCol.find_many(
            {
                "listing_id": listing_id,
                "$or": [{"poster_user_id": user_id}, {"interested_user_id": user_id}],
            }
        )
        if not messages:
            return []

        poster_user = await c.UsersCol.find_one(
            {"user_id": messages[0]["poster_user_id"]}
        )
        interested_user = await c.UsersCol.find_one(
            {"user_id": messages[0]["interested_user_id"]}
        )

        for msg in messages:
            msg["poster_user_name"] = poster_user["nume"]
            msg["poster_user_avatar"] = poster_user["avatar"]
            msg["interested_user_name"] = interested_user["nume"]
            msg["interested_user_avatar"] = interested_user["avatar"]

        return messages

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content=[],
        status=State.FAILED,
        status_code=500,
    )
