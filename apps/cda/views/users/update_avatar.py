import os
from apps.cda.models.collections import UsersCol
from apps.cda.models.user import UserOnAvatarModel
from common.logger import log
from common.responses import CustomResponse, State


async def update_avatar(user_id: str, avatar_image_path: str):
    try:
        image_url = f"/cda/images/{os.path.basename(avatar_image_path)}"
        updated = await UsersCol.update_one(
            {"user_id": user_id},
            data=UserOnAvatarModel(avatar=image_url).model_dump(),
        )
        if updated:
            return CustomResponse(content="Poza a fost incarcata")
    except Exception as err:
        log.exception(err)
    return CustomResponse(
        content="Incearca din nou", status=State.FAILED, status_code=400
    )
