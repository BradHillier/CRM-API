from marshmallow import Schema, fields, post_load, validate, validates, validates_schema, ValidationError
import phonenumbers 

from .models import Customer


class CustomerSchema(Schema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone_number = fields.String()
    email = fields.Email()

    address = fields.String()
    city = fields.String()
    province = fields.String()

    register_date = fields.DateTime()
    expire_date = fields.DateTime()

    @validates('phone_number')
    def validate_phone_number(self, provided_number, **kwargs):
        parsed_number = phonenumbers.parse(provided_number, 'CA')

        # TODO: write a better error messages
        if not phonenumbers.is_possible_number(parsed_number): 
            raise ValidationError('phone number is invalid')
        if len([char for char in provided_number if char.isdigit()]) < 10:
            raise ValidationError('phone number must be at least 10 digits long')

    @post_load
    def format_phone_number(self, customer, many, **kwargs):
        if customer.get('phone_number'):
            parsed_number = phonenumbers.parse(customer['phone_number'], 'CA')
            customer['phone_number'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return customer

    @post_load
    def capitalize(self, customer, many, **kwargs):
        for key in ['first_name', 'last_name', 'city', 'province']:
            if customer.get(key):
                customer[key] = ' '.join([word.capitalize() for word in customer[key].split()])
        return customer

    @validates_schema
    def validate_location(self, data, **kwargs):
        # TODO: may require Google's paid Address Validation API 
        pass

    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)
