from database.models import Bookmark
from resources.crud import CRUDListApi, CRUDItemApi


class BookmarksApi(CRUDListApi):
    model_class = Bookmark
        
class BookmarkApi(CRUDItemApi):
    model_class = Bookmark
