from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Office(Base):
    __tablename__ = 'offices'

    office_id = Column(Integer, primary_key=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

class EstateAgent(Base):
    __tablename__ = 'estate_agents'

    agent_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)

class AgentOffice(Base):
    __tablename__ = 'agent_office'

    agent_office_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    office_id = Column(Integer, ForeignKey('offices.office_id'))

class Seller(Base):
    __tablename__ = 'sellers'

    seller_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)

class Listing(Base):
    __tablename__ = 'listings'

    listing_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('sellers.seller_id'))
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    listing_price = Column(Float)
    zip_code = Column(String)
    date_of_listing = Column(Date)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    office_id = Column(Integer, ForeignKey('offices.office_id'))
    status = Column(String, default='listed')


class Buyer(Base):
    __tablename__ = 'buyers'

    buyer_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)

class Sale(Base):
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.listing_id'))
    buyer_id = Column(Integer, ForeignKey('buyers.buyer_id'))
    sale_price = Column(Float)
    date_of_sale = Column(Date)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))

class Commission(Base):
    __tablename__ = 'commissions'

    commission_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    sale_id = Column(Integer, ForeignKey('sales.sale_id'))
    commission_amount = Column(Float)
    commission_date = Column(Date)

class MonthlyCommission(Base):
    __tablename__ = 'monthly_commission'

    monthly_commission_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    year = Column(Integer)
    month = Column(Integer)
    total_commission = Column(Float)