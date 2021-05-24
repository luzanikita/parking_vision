from database.models import Status
from resources.crud import CRUDListApi, CRUDItemApi


class StatusesApi(CRUDListApi):
    model_class = Status
        
class StatusApi(CRUDItemApi):
    model_class = Status
