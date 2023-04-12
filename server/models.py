#export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db revision --autogenerate -m 'Create tables' 
# flask db upgrade 

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import MetaData


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    

class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    
    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise AssertionError('Name cannot be empty!')
        return name
    
    @validates('age')
    def validates_age(self, key, age):
        if age <  18:
            raise AssertionError('Age must be greater than 18!')
        return age
    
class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'
    
    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Integer)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    
    tenant = db.relationship('Tenant', backref='leases')
    apartment = db.relationship('Apartment', backref='leases')
    
    serialize_rules = ('-apartments.leases', '-tenants.leases')