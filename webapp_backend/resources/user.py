from database.models import User
from resources.crud import CRUDListApi, CRUDItemApi


class UsersApi(CRUDListApi):
    model_class = User
        
class UserApi(CRUDItemApi):
    model_class = User
