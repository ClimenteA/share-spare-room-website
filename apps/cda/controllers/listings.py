from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, UploadFile, Cookie, Request
from apps.cda.models.listing import (
    ListingOnCreateModel,
    ListingOnUpdateModel,
)
from apps.cda.models.collections import CDACol
import apps.cda.views.listings as views
from common.responses import CustomResponse, State
from common.save_image import save_image
from common.jwt import get_user_id_from_token
from common.render_template import render_template


router = APIRouter(tags=[CDACol.Listings], prefix="/cda")


@router.get("/anunturi")
async def get_listings_response(
    request: Request,
    pagina: int = 1,
    cautare: str = None,
    as_json: bool = False,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    result = await views.get_listings(pagina, cautare, user_id)
    result = {
        "listings": result,
        "logged": user_id,
        "pagina": pagina,
        "cautare": cautare,
    }
    if as_json:
        return result
    return await render_template(request, "cda/listings.html", context=result)


@router.get("/camera-in-apartament/{listing_id}")
async def get_listing_details_template(
    request: Request,
    listing_id: str,
    as_json: bool = False,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    result = await views.get_listings(page=None, search=listing_id, user_id=user_id)
    if as_json:
        return result

    if result:
        return await render_template(
            request,
            "cda/listing_details.html",
            context={"listing": result[0], "logged": user_id},
        )
    return RedirectResponse("/cda/anunturi")


@router.get("/adauga-anunt", response_class=HTMLResponse)
async def get_add_listing_template(
    request: Request,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return RedirectResponse("/cda/autentificare")
    return await render_template(
        request, "cda/add_listing.html", context={"logged": user_id}
    )


@router.post("/create-listing", response_model=CustomResponse)
async def create_listing(
    listing: ListingOnCreateModel,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.create_listing(user_id, listing)
    return result


@router.put("/update-listing", response_model=CustomResponse)
async def update_listing(
    listing: ListingOnUpdateModel,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.update_listing(user_id, listing)
    return result


@router.post("/upload-images", response_model=CustomResponse)
async def upload_images(
    listing_id: str,
    images: list[UploadFile],
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )

    image_paths = []
    for image in images[:3]:
        image_path = await save_image(image, "cda")
        image_paths.append(image_path)

    result = await views.update_images(user_id, listing_id, image_paths)
    return result


@router.delete("/delete-listing/{listing_id}", response_model=CustomResponse)
async def delete_listing(
    listing_id: str,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    return await views.delete_listings(user_id, [listing_id])
