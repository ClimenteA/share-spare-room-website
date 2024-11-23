import apps.cda.models.collections as c
from common.logger import log
from .convert_to_ro_date import convert_to_ro_date


def get_search_query(search: str = None):
    if search is None:
        return {}

    return {
        "$or": [
            {"titlu": {"$regex": search, "$options": "i"}},
            {"oras": {"$regex": search, "$options": "i"}},
            {"zona": {"$regex": search, "$options": "i"}},
            {"descriere": {"$regex": search, "$options": "i"}},
            {"pret": {"$regex": search, "$options": "i"}},
            {"listing_id": {"$regex": search, "$options": "i"}},
            {"user_id": {"$regex": search, "$options": "i"}},
            {"created_at": {"$regex": search, "$options": "i"}},
            {"updated_at": {"$regex": search, "$options": "i"}},
        ]
    }


async def update_listing_with_owner_details(listing: dict):
    listing_owner = await c.UsersCol.find_one({"user_id": listing["user_id"]})

    listing["user_nume"] = listing_owner.get("nume")
    listing["current_user_is_owner"] = False
    listing["user_avatar"] = listing_owner["avatar"]

    return listing


async def update_message_with_users_details(msg: dict):
    poster_user = await c.UsersCol.find_one(
        {"user_id": msg["poster_user_id"]},
        projection={"_id": 0, "user_id": 1, "nume": 1, "descriere": 1, "avatar": 1},
    )
    interested_user = await c.UsersCol.find_one(
        {"user_id": msg["interested_user_id"]},
        projection={"_id": 0, "user_id": 1, "nume": 1, "descriere": 1, "avatar": 1},
    )

    msg["poster_user"] = poster_user
    msg["interested_user"] = interested_user

    return msg


async def normalize_raw_messages(raw_messages: list[dict]):
    messages = []
    for msg in raw_messages:
        msg = await update_message_with_users_details(msg)

        litemsg = {
            "poster_seen_it": msg["poster_seen_it"],
            "interested_seen_it": msg["interested_seen_it"],
            "poster_user_id": msg["poster_user_id"],
            "interested_user_id": msg["interested_user_id"],
            "poster_message": msg["poster_message"],
            "interested_message": msg["interested_message"],
            "poster_user_name": msg["poster_user"]["nume"],
            "interested_user_nume": msg["interested_user"]["nume"],
            "interested_user_descriere": msg["interested_user"]["descriere"],
            "poster_user_avatar": msg["poster_user"]["avatar"],
            "interested_user_avatar": msg["interested_user"]["avatar"],
            "message_id": msg["message_id"],
            "date": convert_to_ro_date(msg["updated_at"]),
        }

        messages.append(litemsg)

    return messages


async def group_messages_by_interested_user(
    user_id: str, messages: list[dict], poster_user: dict = None
):
    grouped_messages = {}
    for msg in messages:
        seen = all([msg["interested_seen_it"], msg["poster_seen_it"]])

        sender_user_id = None

        if poster_user and msg["poster_user_id"] not in grouped_messages:
            grouped_messages[msg["poster_user_id"]] = {
                "poster_user_description": poster_user["descriere"],
                "poster_user_id": poster_user["user_id"],
                "poster_user_nume": poster_user["nume"],
                "poster_user_avatar": poster_user["avatar"],
                "messages": [],
            }

        if poster_user is None and msg["interested_user_id"] not in grouped_messages:
            grouped_messages[msg["interested_user_id"]] = {
                "interested_user_description": msg["interested_user_descriere"],
                "interested_user_id": msg["interested_user_id"],
                "interested_user_nume": msg["interested_user_nume"],
                "interested_user_avatar": msg["interested_user_avatar"],
                "messages": [],
            }

        if msg["poster_message"]:
            name = msg["poster_user_name"]
            sent_msg = msg["poster_message"]
            seen = msg["interested_seen_it"]
            sender_user_id = msg["poster_user_id"]

        if msg["interested_message"]:
            name = msg["interested_user_nume"]
            sent_msg = msg["interested_message"]
            seen = msg["poster_seen_it"]
            sender_user_id = msg["interested_user_id"]

        message = {
            "name": name,
            "date": msg["date"],
            "message": sent_msg,
            "seen": seen,
            "message_id": msg["message_id"],
            "sender_user_id": sender_user_id,
            "original_message": msg,
        }

        if poster_user:
            grouped_messages[msg["poster_user_id"]]["messages"].append(message)
        else:
            grouped_messages[msg["interested_user_id"]]["messages"].append(message)

    grouped_messages_values = list(grouped_messages.values())

    return grouped_messages_values


async def update_listing_with_messages(listing: dict, user_id: str):
    listing["new_messages"] = False

    if user_id is None:
        listing["messages"] = []
        return listing

    listing["current_user_is_owner"] = listing["user_id"] == user_id

    raw_messages = await c.MessagesCol.find_many(
        {
            "listing_id": listing["listing_id"],
            "$or": [
                {"poster_user_id": user_id},
                {"interested_user_id": user_id},
            ],
        }
    )

    messages = await normalize_raw_messages(raw_messages)

    poster_user = None
    if not listing["current_user_is_owner"]:
        poster_user = await c.UsersCol.find_one({"user_id": listing["user_id"]})

    grouped_messages = await group_messages_by_interested_user(
        user_id, messages, poster_user
    )

    if grouped_messages:
        for gmsg in grouped_messages:
            for msg in gmsg["messages"]:
                if msg["seen"] is False and user_id == msg["sender_user_id"]:
                    continue
                if msg["seen"] is False:
                    listing["new_messages"] = True
                    gmsg["new_messages"] = True
                    break

        listing["messages"] = grouped_messages

        return listing

    if not listing["current_user_is_owner"]:
        if poster_user is None:
            poster_user = await c.UsersCol.find_one({"user_id": listing["user_id"]})

        listing["messages"] = [
            {
                "poster_user_description": poster_user["descriere"],
                "poster_user_id": poster_user["user_id"],
                "poster_user_nume": poster_user["nume"],
                "poster_user_avatar": poster_user["avatar"],
                "messages": [],
            }
        ]
        return listing


async def get_listings(
    page: int, search: str = None, user_id: str = None, interested_user_id: str = None
):
    try:
        if interested_user_id is not None:
            listing_ids = await c.MessagesCol.distinct(
                field="listing_id",
                filters={"interested_user_id": interested_user_id},
            )
            query = {"listing_id": {"$in": listing_ids}}
        else:
            query = get_search_query(search)

        listings = await c.ListingsCol.find_many(filters=query, page=page)

        for listing in listings:
            listing["created_at"] = convert_to_ro_date(listing["created_at"])
            listing = await update_listing_with_owner_details(listing)
            listing = await update_listing_with_messages(
                listing, user_id or interested_user_id
            )

        return listings

    except Exception as err:
        log.exception(err)

    return []
