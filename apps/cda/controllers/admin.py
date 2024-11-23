from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from common.responses import CustomResponse, State
from common.logger import log
from common.render_template import render_template
from apps.cda.models.admin import MessageAdminModel
from apps.cda.models.collections import MessagesAdminCol


router = APIRouter(tags=["CDAAdmin"], prefix="/cda/admin")


@router.get("/contact", response_class=HTMLResponse)
async def get_contact_template(request: Request, listing_id: str = None):
    return await render_template(
        request, "cda/contact.html", context={"listing_id": listing_id}
    )


@router.post("/contact", response_model=CustomResponse)
async def save_message_for_admin(message: MessageAdminModel):
    try:
        await MessagesAdminCol.insert_one(message.model_dump())
        return CustomResponse(content="Mesajul tau a fost trimis")
    except Exception as err:
        log.exception(err)
        return CustomResponse(status=State.FAILED, status_code=500)


@router.get("/caut-coleg-apartament", response_class=HTMLResponse)
async def cda_why_this_site_template(request: Request):
    return await render_template(request, "cda/why_this_site.html")
