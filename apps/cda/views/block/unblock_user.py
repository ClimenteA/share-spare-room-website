from common.logger import log
from common.responses import CustomResponse, State
from apps.cda.models.collections import BlockCol, UsersCol


async def unblock_user(user_id: str, block_user_id: str):
    try:
        block_user_exists = await UsersCol.count({"user_id": block_user_id})
        if not block_user_exists:
            return CustomResponse(
                content="Utilizatorul selectat nu exista",
                status=State.FAILED,
                status_code=400,
            )

        deleted = await BlockCol.delete_one(
            {"blocked_by_user_id": user_id, "blocked_user_id": block_user_id}
        )
        if deleted:
            return CustomResponse("Utilizatorul a fost deblocat")

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content="Incearca din nou",
        status=State.FAILED,
        status_code=500,
    )
