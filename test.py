import unittest
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from create import Base, Office, EstateAgent, AgentOffice, Seller, Listing, Buyer, Sale, Commission
from insert import generate_random_data
from queries import get_top_offices, get_average_days_on_market

# Create an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Generate random data for testing
fake = Faker()
generate_random_data(session, fake)

class TestDatabase(unittest.TestCase):
    def test_top_offices(self):
        top_offices = get_top_offices(session, year=2023, month=4)
        self.assertEqual(len(top_offices), 5)

        prev_sales_count = top_offices[0].sales_count
        for office in top_offices[1:]:
            self.assertGreaterEqual(prev_sales_count, office.sales_count)
            prev_sales_count = office.sales_count

    def test_average_days_on_market(self):
        average_days_on_market = get_average_days_on_market(session, year=2023, month=4)
        self.assertGreaterEqual(average_days_on_market, 0)

if __name__ == "__main__":
    unittest.main()
