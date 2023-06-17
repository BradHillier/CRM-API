
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .extensions import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String())
    email = db.Column(db.String())
    address = db.Column(db.String())
    city = db.Column(db.String())
    province = db.Column(db.String())
    register_date = db.Column(db.DateTime, default=datetime.now())
    expire_date = db.Column(db.DateTime, default=datetime.now() + relativedelta(years=1))

    def full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def __repr__(self):
        return f'<Customer(name="{self.first_name} {self.last_name}")>'