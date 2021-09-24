
from flask_restful import Resource
from sqlalchemy import desc

from database.models import Camera, Lot, Status
from resources.crud import CRUDListApi, CRUDItemApi
from resources.errors import ItemNotExistsError

class CamerasApi(CRUDListApi):
    model_class = Camera


class CameraApi(CRUDItemApi):
    model_class = Camera


class CameraStatusApi(Resource):
    def get(self, id):
        camera = Camera.query.filter_by(id=id).first()
        if camera is None:
            raise ItemNotExistsError
        items = {
            "id": id,
            "is_available": camera.is_available,
            "lots": []
        }
        if camera.is_available:
            for lot in Lot.query.filter_by(camera_id=id).all():
                statuses = Status.query.filter_by(lot_id=lot.id)
                if statuses.count() == 0:
                    status = True
                else:
                    status = Status.query\
                        .filter_by(lot_id=lot.id)\
                        .order_by(desc(Status.time))\
                        .first().is_free
            
                item = {
                    "id": lot.id,
                    "x": lot.x,
                    "y": lot.y,
                    "side": lot.side,
                    "is_free": status
                }
                items["lots"].append(item)
                
        return items, 200
