"""
schemas.py uses marshmallow for marshalling to validate the schema and attach
to SQLAlchemy session.
"""
from marshmallow_sqlalchemy import ModelSchema

from models import User
from db import session


class UserSchema(ModelSchema):
    """
    Class for tying user object to marshmallow schema
    """

    class Meta:
        model = User
        sqla_session = session
