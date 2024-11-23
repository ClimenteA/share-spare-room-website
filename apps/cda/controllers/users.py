import os
from typing import Annotated
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi import APIRouter, UploadFile, Cookie, Response, Request
from apps.cda.models.user import (
    UserOnRegisterModel,
    UserOnLoginModel,
    UserOnUpdateModel,
    UsersOnResponseModel,
)
from apps.cda.models.collections import CDACol
import apps.cda.views.users as views
from apps.cda.views import listings
from common.responses import CustomResponse, State
from common.save_image import save_image
from common.jwt import get_user_id_from_token
from common.render_template import render_template
from config import cfg


router = APIRouter(tags=[CDACol.Users], prefix="/cda")


@router.get("/autentificare", response_class=HTMLResponse)
async def get_login_template(
    request: Request,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is not None:
        return RedirectResponse("/cda/contul-meu")
    return await render_template(request, "cda/login.html", context={"logged": user_id})


@router.get("/inregistrare", response_class=HTMLResponse)
async def get_register_template(
    request: Request,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is not None:
        return RedirectResponse("/cda/contul-meu")
    return await render_template(
        request, "cda/register.html", context={"logged": user_id}
    )


@router.get("/contul-meu")
async def get_account_template(
    request: Request,
    as_json: bool = False,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return RedirectResponse("/cda/autentificare")
    user = await views.get_user_by_id(user_id)
    posted_listings = await listings.get_listings(
        page=None, search=user_id, user_id=user_id
    )
    interested_listings = await listings.get_listings(
        page=None, interested_user_id=user_id
    )
    result = {
        "logged": user_id,
        "user": user,
        "posted_listings": posted_listings,
        "interested_listings": interested_listings,
    }
    if as_json:
        return result
    return await render_template(request, "cda/account.html", context=result)


@router.get("/actualizare-cont", response_class=HTMLResponse)
async def get_account_update_template(
    request: Request,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return RedirectResponse("/cda/autentificare")
    user = await views.get_user_by_id(user_id)
    return await render_template(
        request, "cda/account_update.html", context={"user": user, "logged": user_id}
    )


@router.get("/images/{image_name}", response_class=FileResponse)
async def cda_get_image_from_storage(image_name: str):
    filepath = f"{cfg.STORAGE_PATH}/cda/{image_name}"
    if os.path.exists(filepath):
        return FileResponse(filepath)
    return FileResponse("./public/notimg.svg", status_code=404)


@router.get("/users", response_model=list[UsersOnResponseModel])
async def get_users(
    page: int,
    search: str = None,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.get_users(page, search)
    return result


@router.post("/create-user", response_model=CustomResponse)
async def create_user(user: UserOnRegisterModel):
    result = await views.create_user(user)
    return result


@router.post("/login-user", response_model=CustomResponse)
async def login_user(user: UserOnLoginModel, response: Response):
    result = await views.login_user(user)
    response.set_cookie(key="token", value=result.content)
    return result


@router.get("/logout-user")
async def logout_user(
    as_json: bool = False,
    token: Annotated[str | None, Cookie()] = None,
):
    result = await views.logout_user(token)
    if as_json:
        return result
    return RedirectResponse("/cda/autentificare")


@router.put("/update-user", response_model=CustomResponse)
async def update_user(
    user: UserOnUpdateModel,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.update_user(user_id, user)
    return result


@router.post("/upload-avatar", response_model=CustomResponse)
async def upload_avatar(
    avatar: UploadFile,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )

    avatar_image_path = await save_image(avatar, "cda")
    if not avatar_image_path:
        return CustomResponse(
            content="Incearca o alta imagine", status=State.FAILED, status_code=400
        )

    result = await views.update_avatar(user_id, avatar_image_path)
    return result


@router.get("/delete-user")
async def delete_user(
    as_json: bool = False, token: Annotated[str | None, Cookie()] = None
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.delete_user(user_id)
    if as_json:
        return result
    return RedirectResponse("/cda/autentificare")
