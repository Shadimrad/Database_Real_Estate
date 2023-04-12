import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create import Base, Office, EstateAgent, AgentOffice, Seller, Listing, Buyer, Sale, Commission

fake = Faker()

# Create the SQLite database and tables
engine = create_engine("sqlite:///realestate.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Generate random data for Offices, EstateAgents, and AgentOffice
for _ in range(10):
    office = Office(
        address=fake.street_address(),
        city=fake.city(),
        state=fake.state_abbr(),
        zip_code=fake.zipcode(),
    )
    session.add(office)

for _ in range(50):
    agent = EstateAgent(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number(),
    )
    session.add(agent)

session.commit()

all_offices = session.query(Office).all()
all_agents = session.query(EstateAgent).all()

for agent in all_agents:
    for _ in range(random.randint(1, 3)):
        agent_office = AgentOffice(
            agent_id=agent.agent_id,
            office_id=random.choice(all_offices).office_id,
        )
        session.add(agent_office)

session.commit()

# Inserting data for Listings
for _ in range(100):
    seller = Seller(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
    )
    session.add(seller)

    listing = Listing(
        seller_id=seller.seller_id,
        bedrooms=random.randint(1, 5),
        bathrooms=random.randint(1, 4),
        listing_price=random.uniform(50000, 2000000),
        zip_code=fake.zipcode(),
        date_of_listing=fake.date_between(start_date="-2y", end_date="today"),
        agent_id=random.choice(all_agents).agent_id,
        office_id=random.choice(all_offices).office_id,
    )
    session.add(listing)

session.commit()

all_listings = session.query(Listing).all()

# Inserting data for Sales
for listing in all_listings:
    if random.random() < 0.6:  # Assuming 60% of the listings are sold
        buyer = Buyer(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
        )
        session.add(buyer)
        session.flush()  # Get buyer_id assigned

        sale_price = random.uniform(listing.listing_price * 0.9, listing.listing_price * 1.1)
        date_of_sale = listing.date_of_listing + timedelta(days=random.randint(30, 180))

        sale = Sale(
            listing_id=listing.listing_id,
            buyer_id=buyer.buyer_id,
            sale_price=sale_price,
            date_of_sale=date_of_sale,
            agent_id=listing.agent_id,
        )
        session.add(sale)
        session.flush()  # Get sale_id assigned

        # Calculate commission
        if sale_price < 100000:
            commission_rate = 0.1
        elif sale_price < 200000:
            commission_rate = 0.075
        elif sale_price < 500000:
            commission_rate = 0.06
        elif sale_price < 1000000:
            commission_rate = 0.05
        else:
            commission_rate = 0.04

        commission_amount = sale_price * commission_rate

        commission = Commission(
            agent_id=sale.agent_id,
            sale_id=sale.sale_id,
            commission_amount=commission_amount,
        )
        session.add(commission)

        # Mark the original listing as sold
        listing.status = "sold"

session.commit()
