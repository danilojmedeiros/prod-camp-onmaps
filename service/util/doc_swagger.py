from flask_restplus import fields
from service.restplus import api

INPUT_MAIN_SERVICE = api.model(
  'input_main_service', {
        'lat': fields.Float(required=True),
        'lng': fields.Float(required=True)
    }
)