from typing import Annotated
from fastapi import APIRouter, Cookie
from apps.cda.models.collections import CDACol
import apps.cda.views.block as views
from common.responses import CustomResponse, State
from common.jwt import get_user_id_from_token

router = APIRouter(tags=[CDACol.Block], prefix="/cda")


@router.post("/block-user", response_model=CustomResponse)
async def block_user(
    block_user_id: str,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )

    result = await views.block_user(user_id, block_user_id)
    return result


@router.post("/unblock-user", response_model=CustomResponse)
async def unblock_user(
    block_user_id: str,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )

    result = await views.unblock_user(user_id, block_user_id)
    return result
