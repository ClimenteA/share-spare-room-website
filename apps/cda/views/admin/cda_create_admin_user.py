from apps.cda.views.users.create_user import create_user
from config import cfg
from apps.cda.models.user import UserOnRegisterModel


async def cda_create_admin_user():
    user = UserOnRegisterModel(email=cfg.ADMIN_EMAIL, parola=cfg.ADMIN_PASSWORD)
    await create_user(user)
