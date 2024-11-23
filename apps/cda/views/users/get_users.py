import apps.cda.models.collections as c
from common.logger import log
from common.responses import CustomResponse, State


async def get_users(page: int, search: str):
    try:
        query = {}
        if search is not None:
            query = {
                "$or": [
                    {"nume": {"$regex": search, "$options": "i"}},
                    {"descriere": {"$regex": search, "$options": "i"}},
                    {"varsta": {"$regex": search, "$options": "i"}},
                    {"oras": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}},
                    {"user_id": {"$regex": search, "$options": "i"}},
                    {"updated_at": {"$regex": search, "$options": "i"}},
                ]
            }

        users = await c.UsersCol.find_many(filters=query, page=page)

        return users

    except Exception as err:
        log.exception(err)

    return CustomResponse(
        content=[],
        status=State.FAILED,
        status_code=400,
    )
