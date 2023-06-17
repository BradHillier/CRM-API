from api.models import Customer
from flask import json

def test_create_customer(client, app):
    response = client.post('api/customers', 
                headers={'Content-Type': 'application/json'},    
                data=json.dumps({
                    'first_name': 'foo',
                    'last_name': 'bar'
                }))
    with app.app_context():
        assert response.status_code == 201
        assert Customer.query.count() == 1


def test_must_contain_required_parameters(client, app):
    required_fields = ['first_name', 'last_name']

    response = client.post('api/customers', 
                headers={'Content-Type': 'application/json'},    
                data=json.dumps({
                    "phone_number": "123 123 1234",
                    "email": "foo@bar.com",
                    "address": "123 main st",
                    "city": "springfield",
                    "province": "California"
                }))
    with app.app_context():
        assert response.status_code == 400
        assert Customer.query.count() == 0
        for field in required_fields:
            assert response.json.get('error').get(field) == ["Missing data for required field."]

def test_reject_provided_registration_date(client, app):
    response = client.post('api/customers', 
            headers={'Content-Type': 'application/json'},    
            data=json.dumps({
                'first_name': 'foo',
                'last_name': 'bar',
                'register_date': '2023-06-16T03:12:03.875633',
                'expire_date': '2023-06-16T03:12:03.875633'
            }))
    print(response.data)
    with app.app_context():
        assert response.status_code == 400
        assert Customer.query.count() == 0
        for field in ['register_date', 'expire_date']:
            assert response.json.get('error').get(field) == ['Unknown field.']