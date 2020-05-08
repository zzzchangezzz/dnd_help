import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Connection(SqlAlchemyBase):
    __tablename__ = 'spell_and_class'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    spell_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("magic.id"))
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"))
    
    magic = orm.relation('Magic')
    classes = orm.relation('Classes')
