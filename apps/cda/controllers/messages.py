from typing import Annotated
from fastapi import APIRouter, Cookie
from apps.cda.models.message import MessageOnCreateModel, MessageOnResponseModel
from apps.cda.models.collections import CDACol
import apps.cda.views.messages as views
from common.responses import CustomResponse, State
from common.jwt import get_user_id_from_token

router = APIRouter(tags=[CDACol.Messages], prefix="/cda")


@router.get("/messages", response_model=list[MessageOnResponseModel])
async def get_messages(
    listing_id: str,
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.get_messages(user_id, listing_id)
    return result


@router.post("/send-message", response_model=CustomResponse)
async def send_message(
    message: MessageOnCreateModel,
    token: Annotated[str | None, Cookie()] = None,
):
    sender_user_id = await get_user_id_from_token(token)
    if sender_user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )

    result = await views.send_message(sender_user_id, message)
    return result


@router.post("/mark-read-messages", response_model=CustomResponse)
async def mark_read_messages(
    message_ids: list[str],
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.mark_read_messages(user_id, message_ids)
    return result


@router.delete("/delete-messages", response_model=CustomResponse)
async def delete_messages(
    message_ids: list[str],
    token: Annotated[str | None, Cookie()] = None,
):
    user_id = await get_user_id_from_token(token)
    if user_id is None:
        return CustomResponse(
            content="Token invalid", status=State.FAILED, status_code=403
        )
    result = await views.delete_messages(user_id, message_ids)
    return result
