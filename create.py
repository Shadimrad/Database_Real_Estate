from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Office(Base):
    """
    Office model
    
    Attributes:
        office_id (int): Primary key
        address (str): Street address
        city (str): City
        state (str): State
        zip_code (str): Zip code
    """
    __tablename__ = 'offices'

    office_id = Column(Integer, primary_key=True)
    address = Column(String, index=True)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String, index=True)

class EstateAgent(Base):
    """
    Estate agent model
    
    Attributes:
        agent_id (int): Primary key
        first_name (str): First name
        last_name (str): Last name
        email (str): Email
        phone (str): Phone number
    """
    __tablename__ = 'estate_agents'

    agent_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True ,unique=True)
    phone = Column(String, index=True ,unique=True)

class AgentOffice(Base):
    """
    Agent office model
    
    Attributes:
        agent_office_id (int): Primary key
        agent_id (int): Foreign key to estate_agents.agent_id
        office_id (int): Foreign key to offices.office_id
    """
    __tablename__ = 'agent_office'

    agent_office_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    office_id = Column(Integer, ForeignKey('offices.office_id'))

class Seller(Base):
    """
    Seller model
    
    Attributes:
        seller_id (int): Primary key
        name (str): Name
        email (str): Email
        phone (str): Phone number
    """
    __tablename__ = 'sellers'

    seller_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)

class Listing(Base):
    """
    Listing model
    
    Attributes:
        listing_id (int): Primary key
        seller_id (int): Foreign key to sellers.seller_id
        bedrooms (int): Number of bedrooms
        bathrooms (int): Number of bathrooms
        listing_price (float): Listing price
        zip_code (str): Zip code
        date_of_listing (date): Date of listing
        agent_id (int): Foreign key to estate_agents.agent_id
        office_id (int): Foreign key to offices.office_id
        status (str): Status of listing
    """
    __tablename__ = 'listings'

    listing_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('sellers.seller_id'))
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    listing_price = Column(Float, nullable=False)
    zip_code = Column(String)
    date_of_listing = Column(Date, index=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'))
    office_id = Column(Integer, ForeignKey('offices.office_id'), index=True)
    status = Column(String, default='listed')


class Buyer(Base):
    """
    Buyer model
    
    Attributes:
        buyer_id (int): Primary key
        name (str): Name
        email (str): Email
        phone (str): Phone number
    """
    __tablename__ = 'buyers'

    buyer_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)

class Sale(Base):
    """
    Sale model
    
    Attributes:
        sale_id (int): Primary key
        listing_id (int): Foreign key to listings.listing_id
        buyer_id (int): Foreign key to buyers.buyer_id
        sale_price (float): Sale price
        date_of_sale (date): Date of sale
        agent_id (int): Foreign key to estate_agents.agent_id
    """
    __tablename__ = 'sales'

    sale_id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.listing_id'), index=True)
    buyer_id = Column(Integer, ForeignKey('buyers.buyer_id'))
    sale_price = Column(Float)
    date_of_sale = Column(Date, index=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'), index=True)

class Commission(Base):
    """
    Commission model
    
    Attributes:
        commission_id (int): Primary key
        agent_id (int): Foreign key to estate_agents.agent_id
        sale_id (int): Foreign key to sales.sale_id
        commission_amount (float): Commission amount
        commission_date (date): Date of commission
    """
    __tablename__ = 'commissions'

    commission_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'), index=True)
    sale_id = Column(Integer, ForeignKey('sales.sale_id'), index=True)
    commission_amount = Column(Float)
    commission_date = Column(Date)

class MonthlyCommission(Base):
    """
    Monthly commission model
    
    Attributes:
        monthly_commission_id (int): Primary key
        agent_id (int): Foreign key to estate_agents.agent_id
        year (int): Year
        month (int): Month
        total_commission (float): Total commission
    """
    __tablename__ = 'monthly_commission'

    monthly_commission_id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'), index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    total_commission = Column(Float)
