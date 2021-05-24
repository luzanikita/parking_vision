
from database.models import Camera
from resources.crud import CRUDListApi, CRUDItemApi


class CamerasApi(CRUDListApi):
    model_class = Camera
        
class CameraApi(CRUDItemApi):
    model_class = Camera
