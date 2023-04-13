import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create import Base, Office, EstateAgent, AgentOffice, Seller, Listing, Buyer, Sale, Commission, MonthlyCommission

fake = Faker()

def generate_offices(session, num_offices=100):
    offices = []
    for _ in range(num_offices):
        office = Office(
            address=fake.street_address(),
            city=fake.city(),
            state=fake.state_abbr(),
            zip_code=fake.zipcode(),
        )
        insert_data(session, [office])
    return offices

def generate_agents(session, num_agents=50):
    agents = []
    for _ in range(num_agents):
        email=fake.email()
        phone=fake.phone_number()
        if session.query(EstateAgent).filter_by(email=email).first() or session.query(EstateAgent).filter_by(phone=phone).first():
            continue
        agent = EstateAgent(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
            phone=phone,
        )
        insert_data(session, [agent])
    return agents

def generate_agent_offices(session, agents, offices):
    agent_offices = []
    for agent in agents:
        for _ in range(random.randint(1, 3)):
            agent_office = AgentOffice(
                agent_id=agent.agent_id,
                office_id=random.choice(offices).office_id,
            )
            insert_data(session, [agent_office])
    return agent_offices

def generate_listings_and_sellers(session, num_listings=10000, agents=None, offices=None):
    listings = []
    sellers = []
    emails = set()
    phones = set()
    for _ in range(num_listings):
        email = fake.email()
        phone = fake.phone_number()
        if session.query(Seller).filter_by(email=email).first() or session.query(Seller).filter_by(phone=phone).first():
            continue
        if email in emails or phone in phones:
            continue
        emails.add(email)
        phones.add(phone)
        seller = Seller(
            name=fake.name(),
            email=email,
            phone=phone,
        )
        insert_data(session, [seller])

        listing = Listing(
            seller_id=seller.seller_id,
            bedrooms=random.randint(1, 5),
            bathrooms=random.randint(1, 4),
            listing_price=random.uniform(50000, 2000000),
            zip_code=fake.zipcode(),
            date_of_listing=fake.date_between(start_date="-2y", end_date="today"),
            agent_id=random.choice(agents).agent_id,
            office_id=random.choice(offices).office_id,
        )
        insert_data(session, [listing])
    return sellers, listings

def generate_sales_and_commissions(session, listings):
    sales = []
    buyers = []
    emails=set()
    phones=set()
    commissions = []
    for listing in listings:
        if random.random() < 0.6:  # Assuming 60% of the listings are sold
            phone = fake.phone_number()
            email = fake.email()
            if session.query(Buyer).filter_by(email=email).first() or session.query(Buyer).filter_by(phone=phone).first():
                continue
            if email in emails or phone in phones:
                continue
            emails.add(email)
            phones.add(phone)
            buyer = Buyer(
                name=fake.name(),
                email=email,
                phone=phone,
            )
            insert_data(session, [buyer])

            sale_price = random.uniform(listing.listing_price * 0.9, listing.listing_price * 1.1)
            date_of_sale = listing.date_of_listing + timedelta(days=random.randint(30, 180))

            sale = Sale(
                listing_id=listing.listing_id,
                buyer_id=buyer.buyer_id,
                sale_price=sale_price,
                date_of_sale=date_of_sale,
                agent_id=listing.agent_id,
            )
            insert_data(session, [sale])

            commission_rate = get_commission_rate(sale_price)
            commission_amount = sale_price * commission_rate

            commission = Commission(
                agent_id=sale.agent_id,
                sale_id=sale.sale_id,
                commission_amount=commission_amount,
                commission_date=date_of_sale,
            )
            insert_data(session, [commission])

            listing.status = "sold"

    return buyers, sales, commissions

def get_commission_rate(sale_price):
    if sale_price < 100000:
        return 0.1
    elif sale_price < 200000:
        return 0.075
    elif sale_price < 500000:
        return 0.06
    elif sale_price < 1000000:
        return 0.05
    else:
        return 0.04

def insert_data(session, data):
    for item in data:
        session.add(item)
    session.commit()

def main():
    # Create the SQLite database and tables
    engine = create_engine("sqlite:///realestate.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    generate_offices(session)

    generate_agents(session)
    offices = session.query(Office).all()
    agents = session.query(EstateAgent).all()

    generate_agent_offices(session, agents, offices)
    generate_listings_and_sellers(session, agents=agents, offices=offices)
    listings = session.query(Listing).all()
    generate_sales_and_commissions(session, listings)

if __name__ == "__main__":
    main()