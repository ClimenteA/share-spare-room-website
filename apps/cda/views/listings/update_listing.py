from datetime import datetime
from apps.cda.models.listing import ListingOnUpdateModel
from apps.cda.models.collections import ListingsCol, UsersCol
from common.logger import log
from common.responses import CustomResponse, State


async def update_listing(user_id: str, listing: ListingOnUpdateModel):
    try:
        updated = await ListingsCol.update_one(
            filters={"user_id": user_id, "listing_id": listing.listing_id},
            data=listing.model_dump(),
        )
        if updated:
            return CustomResponse(content="Anuntul a fost actualizat")
    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Verifica daca toate campurile sunt completate corect.",
        status=State.FAILED,
        status_code=400,
    )
