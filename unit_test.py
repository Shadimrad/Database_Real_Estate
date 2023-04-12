import unittest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create import Base, Office, EstateAgent, Listing, Buyer, Sale, Commission
from insert import (
    generate_offices,
    generate_agents,
    generate_agent_offices,
    generate_listings_and_sellers,
    generate_sales_and_commissions,
    insert_data
)
import queries

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
        # Insert sample data for testing
        offices = generate_offices(2)
        insert_data(self.session, offices)

        agents = generate_agents(2)
        insert_data(self.session, agents)

        agent_offices = generate_agent_offices(agents, offices)
        insert_data(self.session, agent_offices)

        sellers, listings = generate_listings_and_sellers(2, agents, offices)
        insert_data(self.session, sellers)
        insert_data(self.session, listings)

        buyers, sales, commissions = generate_sales_and_commissions(listings)
        insert_data(self.session, buyers)
        insert_data(self.session, sales)
        insert_data(self.session, commissions)
    
    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_database_structure(self):
        # Check if the required tables are created in the database
        self.assertTrue('offices' in self.engine.table_names())
        self.assertTrue('estate_agents' in self.engine.table_names())
        self.assertTrue('agent_office' in self.engine.table_names())
        self.assertTrue('sellers' in self.engine.table_names())
        self.assertTrue('listings' in self.engine.table_names())
        self.assertTrue('buyers' in self.engine.table_names())
        self.assertTrue('sales' in self.engine.table_names())
        self.assertTrue('commissions' in self.engine.table_names())
    
    def test_insert_data(self):
        # Check if the inserted data is stored correctly in the database
        self.assertEqual(self.session.query(Office).count(), 2)
        self.assertEqual(self.session.query(EstateAgent).count(), 2)
        self.assertEqual(self.session.query(AgentOffice).count(), 2)
        self.assertEqual(self.session.query(Seller).count(), 2)
        self.assertEqual(self.session.query(Listing).count(), 2)
        self.assertEqual(self.session.query(Buyer).count(), 1)
        self.assertEqual(self.session.query(Sale).count(), 1)
        self.assertEqual(self.session.query(Commission).count(), 1)
    
    def test_query_data(self):
        # Call the functions in the queries.py to query the data
        top_offices = queries.get_top_offices(self.session, year=datetime.now().year, month=datetime.now().month)
        top_agents = queries.get_top_agents(self.session, year=datetime.now().year, month=datetime.now().month)
        average_days_on_market = queries.get_average_days_on_market(self.session, year=datetime.now().year, month=datetime.now().month)
        average_selling_price = queries.get_average_selling_price(self.session, year=datetime.now().year, month=datetime.now().month)
        
        # Check if the results are as expected
        self.assertEqual(len(top_offices), 1)
        self.assertEqual(len(top_agents), 1)
        self.assertEqual(average_days_on_market, timedelta(days=0))  # Since we inserted one sale, the average days on the market should be zero
        self.assertEqual(average_selling_price, sales[0].sale_price)  # The average selling price should be equal to the price of the only sale
