import apps.cda.models.collections as c
from common.responses import CustomResponse, State
from config import cfg
from common.logger import log


async def delete_listing(user_id: str, listing_id: str):
    try:
        admin = await c.UsersCol.find_one(
            {"user_id": user_id, "email": cfg.ADMIN_EMAIL}
        )
        if not admin:
            return CustomResponse(
                content="Doar adminii pot executa aceasta operatie",
                status=State.FAILED,
                status_code=403,
            )

        deleted = await c.ListingsCol.delete_one({"listing_id": listing_id})
        if deleted:
            return CustomResponse(content="Anuntul a fost sters")

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Incearca din nou", status=State.FAILED, status_code=500
    )
