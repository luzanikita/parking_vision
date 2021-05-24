from .user import UsersApi, UserApi
from .parking import ParkingsApi, ParkingApi
from .bookmark import BookmarksApi, BookmarkApi
from .camera import CamerasApi, CameraApi
from .lot import LotsApi, LotApi
from .status import StatusesApi, StatusApi


def initialize_routes(api):
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/users/<id>')

    api.add_resource(ParkingsApi, '/api/parkings')
    api.add_resource(ParkingApi, '/api/parkings/<id>')

    api.add_resource(BookmarksApi, '/api/bookmarks')
    api.add_resource(BookmarkApi, '/api/bookmarks/<id>')

    api.add_resource(CamerasApi, '/api/cameras')
    api.add_resource(CameraApi, '/api/cameras/<id>')

    api.add_resource(LotsApi, '/api/lots')
    api.add_resource(LotApi, '/api/lots/<id>')

    api.add_resource(StatusesApi, '/api/status')
    api.add_resource(StatusApi, '/api/status/<id>')
