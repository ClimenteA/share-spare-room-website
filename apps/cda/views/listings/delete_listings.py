from apps.cda.models.collections import ListingsCol, UsersCol
from common.responses import CustomResponse, State
from common.logger import log


async def delete_listings(user_id: str, listing_ids: list[str]):
    try:
        deleted = await ListingsCol.delete_many(
            {"user_id": user_id, "listing_id": {"$in": listing_ids}}
        )
        if deleted:
            await UsersCol.update_one(
                {"user_id": user_id}, data={"$inc": {"anunturi_disponibile": 1}}
            )
            return CustomResponse("Anunturile au fost sterse")
    except Exception as err:
        log.exception(err)
    return CustomResponse(
        "Nu am putut sterge anunturile", status=State.FAILED, status_code=400
    )
