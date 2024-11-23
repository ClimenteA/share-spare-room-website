from common.collections import get_collection, Col


class CDACol(Col):
    Users = "CDAUsers"
    Listings = "CDAListings"
    Messages = "CDAMessages"
    MessagesAdmin = "CDAMessagesAdmin"
    Block = "CDABlock"
    TokenBlackList = "CDATokenBlackList"
    MathUserCheck = "CDAMathUserCheck"


MessagesAdminCol = get_collection(CDACol.MessagesAdmin)
ListingsCol = get_collection(CDACol.Listings)
UsersCol = get_collection(CDACol.Users)
MessagesCol = get_collection(CDACol.Messages)
BlockCol = get_collection(CDACol.Block)
