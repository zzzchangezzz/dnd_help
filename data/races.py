import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Races(SqlAlchemyBase):
    __tablename__ = 'races'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    def __repr__(self):
        return self.name + "\n" + self.description + "\n"
