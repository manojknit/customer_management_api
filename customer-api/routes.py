from flask import jsonify, request, abort
from . import app
from .models import Customer
from .database import SessionLocal
import re

# Function to validate phone number
def validate_phone_number(phone_number):
    pattern = re.compile(r"^\+?1?\d{9,15}$")  # Adjust regex as needed
    return pattern.match(phone_number)

@app.route('/customers', methods=['GET'])
def get_all_customers():
    db = SessionLocal()
    customers = db.query(Customer).all()
    db.close()
    return jsonify([{
        'id': customer.id,
        'full_name': customer.full_name,
        'email': customer.email,
        'phone_number': customer.phone_number
    } for customer in customers])

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    db = SessionLocal()
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    db.close()
    if customer is None:
        abort(404)
    return jsonify({
        'id': customer.id,
        'full_name': customer.full_name,
        'email': customer.email,
        'phone_number': customer.phone_number
    })

@app.route('/customers/email/<string:email>', methods=['GET'])
def get_customer_by_email(email):
    db = SessionLocal()
    customer = db.query(Customer).filter(Customer.email == email).first()
    db.close()
    if customer is None:
        abort(404)
    return jsonify({
        'id': customer.id,
        'full_name': customer.full_name,
        'email': customer.email,
        'phone_number': customer.phone_number
    })

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    if not validate_phone_number(data.get('phone_number')):
        return jsonify({"error": "Invalid phone number"}), 400
    
    new_customer = Customer(
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number']
    )
    
    db = SessionLocal()
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    db.close()
    
    return jsonify({
        'id': new_customer.id,
        'full_name': new_customer.full_name,
        'email': new_customer.email,
        'phone_number': new_customer.phone_number
    }), 201

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    db = SessionLocal()
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        db.close()
        abort(404)

    if 'phone_number' in data and not validate_phone_number(data['phone_number']):
        return jsonify({"error": "Invalid phone number"}), 400

    customer.full_name = data.get('full_name', customer.full_name)
    customer.email = data.get('email', customer.email)
    customer.phone_number = data.get('phone_number', customer.phone_number)

    db.commit()
    db.close()

    return jsonify({
        'id': customer.id,
        'full_name': customer.full_name,
        'email': customer.email,
        'phone_number': customer.phone_number
    })

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    db = SessionLocal()
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        db.close()
        abort(404)

    db.delete(customer)
    db.commit()
    db.close()
    
    return jsonify({"message": "Customer deleted successfully"}), 204

  