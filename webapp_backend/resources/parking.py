from database.models import Parking
from resources.crud import CRUDListApi, CRUDItemApi


class ParkingsApi(CRUDListApi):
    model_class = Parking
        
class ParkingApi(CRUDItemApi):
    model_class = Parking
