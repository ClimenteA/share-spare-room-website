import os
from apps.cda.models.listing import ListingOnImageUpdateModel
from apps.cda.models.collections import ListingsCol
from common.responses import CustomResponse, State
from common.logger import log


async def update_images(user_id: str, listing_id: str, image_paths: list[str]):
    try:
        img_url = lambda path: f"/cda/images/{os.path.basename(path)}"

        images = ListingOnImageUpdateModel(
            img1=img_url(image_paths[0]),
            img2=img_url(image_paths[1]) if len(image_paths) > 1 else None,
            img3=img_url(image_paths[2]) if len(image_paths) > 2 else None,
        )

        updated = await ListingsCol.update_one(
            {"user_id": user_id, "listing_id": listing_id}, data=images.model_dump()
        )

        if updated:
            return CustomResponse(content="Pozele au fost incarcate")

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Pozele nu au putut fi incarcate",
        status=State.FAILED,
        status_code=500,
    )
