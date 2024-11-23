from .users import router as UserR
from .listings import router as ListingR
from .messages import router as MessageR
from .block_user import router as BlockR
from .admin import router as AdminR
from .legal import router as CDALegalR

routers = [UserR, ListingR, MessageR, BlockR, AdminR, CDALegalR]
