from flask import request
from flask_restful import Resource

from database.db import db
from sqlalchemy.exc import IntegrityError
from resources.errors import ItemNotExistsError, SchemaValidationError

class CRUDModel():
    def json(self):
        if self is None:
            raise ItemNotExistsError
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @classmethod
    def add_item(cls, body):
        new_item = cls(**body)
        db.session.add(new_item)
        db.session.commit()
        return new_item
    
    @classmethod
    def get_all_items(cls):
        return [cls.json(item) for item in cls.query.all()]

    @classmethod
    def get_item(cls, id):
        return cls.json(cls.query.filter_by(id=id).first())

    @classmethod
    def update_item(cls, id, body):
        item_to_update = cls.query.filter_by(id=id).first()
        if item_to_update is None:
            raise ItemNotExistsError

        for attr_name in dir(item_to_update):
            if attr_name.startswith('__'):
                continue
            item_attr = getattr(item_to_update, attr_name)
            setattr(item_to_update, attr_name, body.get(attr_name, item_attr))

        db.session.commit()
    
    @classmethod
    def delete_item(cls, id):
        item_to_delete = cls.query.filter_by(id=id)
        if item_to_delete.first() is None:
            raise ItemNotExistsError

        item_to_delete.delete()
        db.session.commit()


class CRUDListApi(Resource):
    def get(self):
        items = {self.model_class.__tablename__: self.model_class.get_all_items()}
        return items, 200

    def post(self):
        try:
            body = request.get_json()
            item = self.model_class.add_item(body)
            return {'id': item.id}, 200
        except IntegrityError:
            raise SchemaValidationError

        
class CRUDItemApi(Resource):
    def put(self, id):
        body = request.get_json()
        self.model_class.update_item(id, body)
        return 'Item updated.', 200
    
    def delete(self, id):
        self.model_class.delete_item(id)
        return 'Item deleted.', 200

    def get(self, id):
        item = self.model_class.get_item(id)
        return item, 200
