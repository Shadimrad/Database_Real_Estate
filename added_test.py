import unittest
from datetime import date
from create import Base, Office, EstateAgent, AgentOffice, Seller, Listing, Buyer, Sale, Commission
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from insert import generate_offices, generate_agents, generate_agent_offices, generate_listings_and_sellers, generate_sales_and_commissions, insert_data
from queries import get_top_offices, get_top_agents, get_average_days_on_market, get_average_selling_price

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """
        Setting up the database for testing
        """
        # Create an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Generate and insert sample data
        offices = generate_offices(2)
        agents = generate_agents(4)
        agent_offices = generate_agent_offices(agents, offices)
        sellers, listings = generate_listings_and_sellers(10, agents, offices)
        buyers, sales, commissions = generate_sales_and_commissions(listings)
        insert_data(self.session, offices + agents + agent_offices + sellers + listings + buyers + sales + commissions)

    def test_get_top_offices(self):
        """
        Testing the get_top_offices
        """
        result = get_top_offices(self.session, date.today().year, date.today().month)
        self.assertIsNotNone(result)

    def test_top_agents(self):
        """
        Testing the get_top_agents
        """
        result = get_top_agents(self.session, date.today().year, date.today().month)
        self.assertIsNotNone(result)

    def test_get_average_days_on_market(self):
        """
        Testing the get_average_days_on_market
        """
        result = get_average_days_on_market(self.session, date.today().year, date.today().month)
        self.assertIsNotNone(result)

    def test_get_average_selling_price(self):
        """
        Testing the get_average_selling_price
        """
        result = get_average_selling_price(self.session, date.today().year, date.today().month)
        self.assertIsNotNone(result)

    def tearDown(self):
        """
        Clean up the database after each test
        """
        self.session.close()
        Base.metadata.drop_all(self.engine)

if __name__ == '__main__':
    unittest.main()
