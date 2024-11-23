import apps.cda.models.collections as c
from config import cfg
from common.responses import CustomResponse, State
from common.logger import log


async def delete_user(user_id: str, to_delete_user_id: str):
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

        if user_id == to_delete_user_id:
            return CustomResponse(
                content="Trebuie sa ramana un admin in baza de date",
                status=State.FAILED,
                status_code=400,
            )

        deleted_user = await c.UsersCol.delete_one({"user_id": to_delete_user_id})
        await c.ListingsCol.delete_many({"user_id": to_delete_user_id})
        if deleted_user:
            return CustomResponse(content="Utilizatorul a fost sters")

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Incearca din nou", status=State.FAILED, status_code=500
    )
