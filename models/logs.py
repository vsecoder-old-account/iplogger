import sqlalchemy as sa
from .db_session import SqlAlchemyBase

class Logs(SqlAlchemyBase):
    __tablename__ = 'logs'

    id = sa.Column(sa.Integer,
                   primary_key=True)
    url = sa.Column(sa.String, nullable=True)
    data = sa.Column(sa.String, nullable=True)
    password = sa.Column(sa.String, nullable=True)
