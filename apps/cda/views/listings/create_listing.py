from datetime import datetime
from apps.cda.models.listing import ListingOnCreateModel, ListingOnDbModel
from apps.cda.models.collections import ListingsCol, UsersCol
from common.logger import log
from common.responses import CustomResponse, State


async def create_listing(user_id: str, listing: ListingOnCreateModel):
    try:
        listing = ListingOnDbModel(
            user_id=user_id,
            created_at=datetime.utcnow().isoformat(),
            **listing.model_dump()
        )

        user_query = {"user_id": user_id}
        user = await UsersCol.find_one(
            user_query, projection={"_id": 0, "anunturi_disponibile": 1}
        )
        posted_listings = await ListingsCol.count(user_query)
        if posted_listings >= user["anunturi_disponibile"]:
            return CustomResponse(
                content="Doar un anunt postat este gratis.",
                status=State.FAILED,
                status_code=403,
            )

        updated_listing = await ListingsCol.insert_one(listing.model_dump())

        if updated_listing:
            await UsersCol.update_one(
                user_query, data={"$inc": {"anunturi_disponibile": -1}}
            )
            return CustomResponse(
                content="Anuntul a fost adaugat", extra=listing.listing_id
            )

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Verifica daca toate campurile sunt completate corect.",
        status=State.FAILED,
        status_code=400,
    )
