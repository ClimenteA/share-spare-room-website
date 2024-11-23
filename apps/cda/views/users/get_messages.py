from common.logger import log
import apps.cda.models.collections as c


async def get_messages(user_id: str):
    try:
        messages = await c.MessagesCol.find_many(
            {"$or": [{"poster_user_id": user_id}, {"interested_user_id": user_id}]}
        )
        if not messages:
            return []

        message_listing_ids = await c.MessagesCol.distinct(
            field="listing_id",
            filters={
                "$or": [{"poster_user_id": user_id}, {"interested_user_id": user_id}]
            },
        )

        listings = await c.ListingsCol.find_many(
            filters={"listing_id": {"$in": message_listing_ids}}
        )

        for l in listings:
            for m in messages:
                if l["listing_id"] == m["listing_id"]:
                    if "messages" not in l:
                        l["messages"] = []
                    l["messages"].append(m)

                    listing_owner = await c.UsersCol.find_one({"user_id": l["user_id"]})
                    l["user_avatar"] = listing_owner.get("avatar")
                    l["user_nume"] = listing_owner.get("nume")

        return listings

    except Exception as err:
        log.exception(err)
    return []
