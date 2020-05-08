import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Magic(SqlAlchemyBase):
    __tablename__ = 'magic'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    level = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    distance = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    components = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    durability = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    classes = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    
    connect = orm.relation("Connection", back_populates='magic')
    
    def __repr__(self):
        return self.title + "\nУровень: " + self.level + "\nДистанция: " + \
               self.distance + "\nКомпоненты: " + self.components +\
               "\nДлительность:" + self.durability + "\nКлассы: " +\
               self.classes + "\nОписание: \n" + self.content
