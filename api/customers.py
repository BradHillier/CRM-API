from flask import Blueprint, request
from marshmallow import ValidationError
from .models import Customer
from .extensions import db
from .serializers import CustomerSchema


customers_bp = Blueprint('customers', __name__, url_prefix="/api")


@customers_bp.route('/customers', methods=['POST', 'GET'])
def handle_customers():
    schema = CustomerSchema()

    if request.method == 'POST':
        if request.is_json:
            try:
                # initial registration date and expiration date are automatically determined
                new_customer = CustomerSchema(exclude=['register_date', 'expire_date']).load(request.get_json())
                db.session.add(new_customer)
                db.session.commit()
                return {'message': f'successfully registered {new_customer.full_name()} as a new customer'}, 201
            except ValidationError as error:
                return {'error': error.messages}, 400
        else:
            return {'error': f'The request payload is not in JSON format'}, 400

    elif request.method == 'GET':

        # filter search results based on provided parameters
        criteria = request.args.to_dict()
        customers = db.session.query(Customer)
        for attribute, search_parameter in criteria.items():

            # ignore case when filtering
            customers = customers.filter(getattr(Customer, attribute).ilike(f'%{search_parameter}%'))

        # serialize filtered customers into JSON
        return {'customers': [schema.dump(customers, many=True)]}, 200

@customers_bp.route('/customers/<int:id>', methods=['PUT', 'DELETE'])
def handle_update_customer():
    pass