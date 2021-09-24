from .user import UsersApi, UserApi
from .parking import ParkingsApi, ParkingApi
from .bookmark import BookmarksApi, BookmarkApi
from .camera import CamerasApi, CameraApi, CameraStatusApi
from .lot import LotsApi, LotApi
from .status import StatusesApi, StatusApi


def initialize_routes(api):
    api.add_resource(UsersApi, '/api/v1/users')
    api.add_resource(UserApi, '/api/v1/users/<id>')

    api.add_resource(ParkingsApi, '/api/v1/parkings')
    api.add_resource(ParkingApi, '/api/v1/parkings/<id>')

    api.add_resource(BookmarksApi, '/api/v1/bookmarks')
    api.add_resource(BookmarkApi, '/api/v1/bookmarks/<id>')

    api.add_resource(CamerasApi, '/api/v1/cameras')
    api.add_resource(CameraApi, '/api/v1/cameras/<id>')
    api.add_resource(CameraStatusApi, '/api/cameras/<id>/status')

    api.add_resource(LotsApi, '/api/v1/lots')
    api.add_resource(LotApi, '/api/v1/lots/<id>')

    api.add_resource(StatusesApi, '/api/v1/status')
    api.add_resource(StatusApi, '/api/v1/status/<id>')
