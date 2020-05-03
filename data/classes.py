import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

class Classes(SqlAlchemyBase):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    
    def __repr__(self):
        return self.title + "\n" + self.content + "\n"