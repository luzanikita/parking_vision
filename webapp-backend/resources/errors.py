class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class ItemAlreadyExistsError(Exception):
    pass

class UpdatingItemError(Exception):
    pass

class DeletingItemError(Exception):
    pass

class ItemNotExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "ItemAlreadyExistsError": {
         "message": "Item with given name already exists",
         "status": 400
     },
     "UpdatingItemError": {
         "message": "Updating item added by other is forbidden",
         "status": 403
     },
     "DeletingItemError": {
         "message": "Deleting item added by other is forbidden",
         "status": 403
     },
     "ItemNotExistsError": {
         "message": "Item with given id doesn't exists",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     }
}
