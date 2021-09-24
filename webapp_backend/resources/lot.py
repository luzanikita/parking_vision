from database.models import Lot
from resources.crud import CRUDListApi, CRUDItemApi


class LotsApi(CRUDListApi):
    model_class = Lot
        
class LotApi(CRUDItemApi):
    model_class = Lot
