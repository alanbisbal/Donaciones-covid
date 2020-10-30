from app import db
from flask import request

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models import permiso, user, users_rols, rols_permisos


class Rol(db.Model):
    __tablename__ = 'rols'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    users = db.relationship("User" , secondary="users_rols")
    permisos = db.relationship("Permiso", secondary="rols_permisos")

    def __init__(self, data):
        self.name = data['name']
        self.description = data['description']
        db.session.commit()

    @classmethod
    def __str__(self):
        return '<Rol {}>'.format(self.name)

    def all():
        return db.session.query(Rol).all()

    def permission_names(self):
        return [permiso.name for permiso in self.permisos]

    def has_permit(self, permit_name):
        """ Obtiene los permisos y devuelve un boolean
        respecto al nombre del permisos que se paso por parametro """
        permits = map(lambda p: p.name == permit_name, self.permisos)
        return any(permits)

    def except_rols(roles):
        allrols = db.session.query(Rol).all()
        return (set(allrols)-set(roles))
