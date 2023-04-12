from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False
app.json.compact = False

migrate = Migrate( app, db )

db.init_app( app )
api = Api( app )

class All_Apartments(Resource):
    def get(self):
        all_apartments = Apartment.query.all()
        apartment_list = []
        for apartment in all_apartments:
            new_apartment = {
                'id' : apartment.id,
                'number' : apartment.number
            }
            apartment_list.append(new_apartment)

    def post(self):
        data = request.get_json()
        apartment = Apartment(number=data['number'])
        db.session.add(apartment)
        db.session.commit()
        return make_response("apartment added", 201)
    
api.add_resource(All_Apartments, '/apartments')       

class Apartment_By_Id(Resource):
    def get(self, id):
        apartment = Apartment.query.filter_by(id=id).first()
        if not apartment:
            return make_response(jsonify({'error': 'Apartment not found'}), 404)
        response = make_response(apartment.to_dict(), 200)
        return response
    
    def patch(self, id):
        apartment = Apartment.query.filter_by(id=id).first()
        data = request.get_json()
        for attr, value in data.items():
            setattr(apartment, attr, value)
        db.session.add(apartment)
        db.session.commit()
        
        response = make_response(apartment.to_dict(), 200)
        return response

    def delete(self, id):
        apartment = Apartment.query.filter_by(id=id).first()
        if not apartment:
            return make_response("apartment not found", 404)
        db.session.delete(apartment)
        db.session.commit()
        return make_response("apartment deleted", 200)


api.add_resource(Apartment_By_Id, '/apartments/<int:id>')



class All_Tenants(Resource):
    def get(self):
        all_tenants = Tenant.query.all()
        tenant_list = []
        for tenant in all_tenants:
            new_tenant = {
                'id' : tenant.id,
                'name' : tenant.name,
                'age' : tenant.age
            }
            tenant_list.append(new_tenant)
            
    def post(self):
        data = request.get_json()
        tenant = Tenant(name=data['name'], age=request.get_json()['age'])
        db.session.add(tenant)
        db.session.commit()
        return make_response(tenant.to_dict(), 201)
    
api.add_resource(All_Tenants, '/tenants')
    
class Tenant_By_Id(Resource):
    def get(self, id):
        tenant = Tenant.query.filter_by(id=id).first()
        if not tenant:
            return make_response(jsonify({'error': 'Tenant not found'}), 404)
        response = make_response(tenant.to_dict(), 200)
        return response
    
    def delete(self, id):
        tenant = Tenant.query.filter_by(id=id).first()
        if not tenant:
            return make_response("tenant not found", 404)
        db.session.delete(tenant)
        db.session.commit()
        return make_response("tenant deleted", 200)
    
    def patch(self, id):
        tenant = Tenant.query.filter_by(id=id).first()
        data = request.get_json()
        for attr, value in data.items():
            setattr(tenant, attr, value)
        db.session.add(tenant)
        db.session.commit()
        
        response = make_response(tenant.to_dict(), 200)
        return response

api.add_resource(Tenant_By_Id, '/tenants/<int:id>')

class All_Leases(Resource):
    def get(self):
        all_leases = Lease.query.all()
        lease_list = []
        for lease in all_leases:
            new_lease = {
                'id' : lease.id,
                'rent' : lease.rent,
                'tenant_id' : lease.tenant_id,
                'apartment_id' : lease.apartment_id
            }
            lease_list.append(new_lease)

    def post(self):
        data = request.get_json()
        lease = Lease(rent=data['rent'], tenant_id=data['tenant_id'], apartment_id=data['apartment_id'])
        db.session.add(lease)
        db.session.commit()
        return make_response("lease added", 201)
    
api.add_resource(All_Leases, '/leases')

class Lease_By_Id(Resource):
    def delete(self, id):
        lease = Lease.query.filter_by(id=id).first()
        if not lease:
            return make_response("lease not found", 404)
        db.session.delete(lease)
        db.session.commit()
        return make_response("lease deleted", 200)
    

api.add_resource(Lease_By_Id, '/leases/<int:id>')
if __name__ == '__main__':
    app.run( port = 3000, debug = True )