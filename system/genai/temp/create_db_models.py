# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class Customer(Base):
    """description: Table to store customer information."""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    credit_limit = Column(DECIMAL, nullable=False, default=1000.0)
    balance = Column(DECIMAL, nullable=True, default=0.0)


class Order(Base):
    """description: Table to store order details, including notes."""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    order_date = Column(DateTime, nullable=False)
    total_amount = Column(DECIMAL, nullable=True, default=0.0)
    notes = Column(String, nullable=True)


class Product(Base):
    """description: Table to store product details."""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)


class Item(Base):
    """description: Table to store items within an order, linking products and orders."""
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL, nullable=True) # Derived from Product
    amount = Column(DECIMAL, nullable=True, default=0.0) # Derived field: quantity * unit_price


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    Customer(name="Alice", email="alice@example.com", credit_limit=1500.0, balance=150.0)
    Customer(name="Bob", email="bob@example.com", credit_limit=2000.0, balance=200.0)
    Customer(name="Carol", credit_limit=2200.0, balance=300.0)
    Customer(name="Dave", email="dave@example.com", credit_limit=2500.0, balance=450.0)
    Order(customer_id=1, order_date=datetime(2023, 10, 5), total_amount=150.0, notes="First order")
    Order(customer_id=2, order_date=datetime(2023, 10, 6), total_amount=200.0)
    Order(customer_id=3, order_date=datetime(2023, 10, 7), total_amount=300.0, notes="Urgent")
    Order(customer_id=4, order_date=datetime(2023, 10, 8), total_amount=450.0)
    Product(name="Laptop", price=1200.0)
    Product(name="Mouse", price=25.0)
    Product(name="Keyboard", price=50.0)
    Product(name="Monitor", price=300.0)
    Item(order_id=1, product_id=1, quantity=1, unit_price=1200.0, amount=1200.0)
    Item(order_id=1, product_id=2, quantity=2, unit_price=25.0, amount=50.0)
    Item(order_id=2, product_id=3, quantity=1, unit_price=50.0, amount=50.0)
    Item(order_id=3, product_id=4, quantity=2, unit_price=300.0, amount=600.0)
    
    
    
    session.add_all([customer1, customer2, customer3, customer4, order1, order2, order3, order4, product1, product2, product3, product4, item1, item2, item3, item4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
