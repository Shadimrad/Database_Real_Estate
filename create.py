from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Office(Base):
    __tablename__ = 'offices'

    office_id = Column(Integer, primary_key=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    agents = relationship('EstateAgent', back_populates='office')

class EstateAgent(Base):
    __tablename__ = 'estate_agents'

    agent_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    office_id = Column(Integer, ForeignKey('offices.office_id'))

    office = relationship('Office', back_populates='agents')
    # listings = relationship('Listing', back_populates='agent')
    # sales = relationship('Sale', back_populates='agent')
    # commissions = relationship('Commission', back_populates='agent')

class Listing(Base):
    __tablename__ = 'listings'

    listing_id = Column(Integer, primary_key=True)
    seller_name = Column(String)
    seller_email = Column(String)
    seller_phone = Column(String)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    listing_price = Column(Float)
    zip_code = Column(String)
    date_of_listing = Column(Date)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    office_id = Column(Integer, ForeignKey('offices.office_id'))
    status = Column(String, default='listed')

    agent = relationship('EstateAgent', back_populates='listings')
    # sales = relationship('Sale', back_populates='listing')

class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.listing_id'))
    buyer_name = Column(String)
    buyer_email = Column(String)
    buyer_phone = Column(String)
    sale_price = Column(Float)
    date_of_sale = Column(Date)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))

    agent = relationship('EstateAgent', back_populates='sales')
    # listing = relationship('Listing', back_populates='sales')
    commission = relationship('Commission', uselist=False, back_populates='sale')

class Commission(Base):
    __tablename__ = 'commissions'

    commission_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    sale_id = Column(Integer, ForeignKey('sales.sale_id'))
    commission_amount = Column(Float)

    agent = relationship('EstateAgent', back_populates='commissions')
    sale = relationship('Sale', back_populates='commission')

# Create the database
engine = create_engine('sqlite:///realestate.db')
Base.metadata.create_all(engine)


# Step 3: Functions to insert listing and update listing when sold
def insert_listing(listing_data):
    ...

def update_listing_when_sold(sale_data):
    ...

# Step 4: SQL queries for generating monthly reports
def top_5_offices():
    ...

def top_5_agents():
    ...

def agent_commissions():
    ...

def average_days_on_market():
    ...

def average_selling_price():
    ...
