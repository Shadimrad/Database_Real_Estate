import unittest
import io
import sys
from contextlib import redirect_stdout
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create import Base, Office, EstateAgent, Listing, Sale, Commission, MonthlyCommission
from queries import get_top_offices, get_top_agents, get_average_days_on_market, get_average_selling_price, insert_monthly_commissions, print_monthly_commissions

class TestQueries(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Add predetermined data here
        self.add_test_data()

    def add_test_data(self):
        offices = [
            Office(address='123 Main St', city='New York', state='NY', zip_code='10001'),
            Office(address='456 Second Ave', city='Los Angeles', state='CA', zip_code='90001'),
            Office(address='789 Market St', city='San Francisco', state='CA', zip_code='94102'),
            Office(address='111 First St', city='Chicago', state='IL', zip_code='60601'),
            Office(address='333 Elm St', city='Boston', state='MA', zip_code='02108')
        ]

        agents = [
            EstateAgent(first_name='John', last_name='Doe', email='john@example.com', phone='1234567890'),
            EstateAgent(first_name='Jane', last_name='Doe', email='jane@example.com', phone='0987654321'),
            EstateAgent(first_name='Michael', last_name='Smith', email='michael@example.com', phone='2345678901'),
            EstateAgent(first_name='Michelle', last_name='Johnson', email='michelle@example.com', phone='9012345678'),
            EstateAgent(first_name='William', last_name='Brown', email='william@example.com', phone='3456789012')
        ]

        today = date.today()
        listings = [
            Listing(seller_id=1, bedrooms=3, bathrooms=2, listing_price=500000, zip_code='10001', date_of_listing=today - timedelta(days=10), agent_id=1, office_id=1),
            Listing(seller_id=2, bedrooms=4, bathrooms=3, listing_price=750000, zip_code='90001', date_of_listing=today - timedelta(days=15), agent_id=2, office_id=2),
            Listing(seller_id=3, bedrooms=2, bathrooms=1, listing_price=450000, zip_code='94102', date_of_listing=today - timedelta(days=20), agent_id=3, office_id=3),
            Listing(seller_id=4, bedrooms=5, bathrooms=4, listing_price=900000, zip_code='60601', date_of_listing=today - timedelta(days=25), agent_id=4, office_id=4),
            Listing(seller_id=5, bedrooms=3, bathrooms=2, listing_price=550000, zip_code='02108', date_of_listing=today - timedelta(days=30), agent_id=5, office_id=5)
        ]

        sales = [
            Sale(listing_id=1, buyer_id=1, sale_price=480000, date_of_sale=today , agent_id=1),
            Sale(listing_id=2, buyer_id=2, sale_price=740000, date_of_sale=today , agent_id=2),
            Sale(listing_id=3, buyer_id=3, sale_price=430000, date_of_sale=today , agent_id=3),
            Sale(listing_id=4, buyer_id=4, sale_price=870000, date_of_sale=today , agent_id=4),
            Sale(listing_id=5, buyer_id=5, sale_price=520000, date_of_sale=today , agent_id=5)
        ]

        self.session.add_all(offices)
        self.session.add_all(agents)
        self.session.add_all(listings)
        self.session.add_all(sales)
        self.session.commit()

    def test_get_top_offices(self):
        year = date.today().year
        month = date.today().month
        top_offices = get_top_offices(self.session, year, month)
        self.assertIsNotNone(top_offices)

    def test_get_top_agents(self):
        year = date.today().year
        month = date.today().month
        top_agents = get_top_agents(self.session, year, month)
        self.assertIsNotNone(top_agents)

    def test_get_average_days_on_market(self):
        year = date.today().year
        month = date.today().month
        avg_days_on_market = get_average_days_on_market(self.session, year, month)
        self.assertIsNotNone(avg_days_on_market)

    def test_get_average_selling_price(self):
        year = date.today().year
        month = date.today().month
        avg_selling_price = get_average_selling_price(self.session, year, month)
        self.assertIsNotNone(avg_selling_price)

    def test_insert_monthly_commissions(self):
        year = date.today().year
        month = date.today().month
        insert_monthly_commissions(self.session, year, month)
        commissions = self.session.query(MonthlyCommission).filter(MonthlyCommission.year == year, MonthlyCommission.month == month).all()
        self.assertIsNotNone(commissions)

    def test_print_monthly_commissions(self):
        year = date.today().year
        month = date.today().month
        insert_monthly_commissions(self.session, year, month)
        monthly_commissions = self.session.query(MonthlyCommission).filter(MonthlyCommission.year == year, MonthlyCommission.month == month).all()

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            print_monthly_commissions(self.session, monthly_commissions)

        expected_output = "1 - John Doe - 24000\n2 - Jane Doe - 37000\n3 - Michael Smith - 21500\n4 - Michelle Johnson - 43500\n5 - William Brown - 26000\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_get_top_offices(self):
        year = date.today().year
        month = date.today().month
        top_offices = get_top_offices(self.session, year, month)
        self.assertEqual(len(top_offices), 5)
        self.assertEqual(top_offices[0].id, 1)

    def test_get_top_agents(self):
        year = date.today().year
        month = date.today().month
        top_agents = get_top_agents(self.session, year, month)
        self.assertEqual(len(top_agents), 5)
        self.assertEqual(top_agents[0].id, 1)

    def test_get_average_days_on_market(self):
        year = date.today().year
        month = date.today().month
        avg_days_on_market = get_average_days_on_market(self.session, year, month)
        self.assertEqual(avg_days_on_market, 20)

    def test_get_average_selling_price(self):
        year = date.today().year
        month = date.today().month
        avg_selling_price = get_average_selling_price(self.session, year, month)
        self.assertEqual(avg_selling_price, 608000)

    def test_insert_monthly_commissions(self):
        year = date.today().year
        month = date.today().month
        insert_monthly_commissions(self.session, year, month)
        commissions = self.session.query(MonthlyCommission).filter(MonthlyCommission.year == year, MonthlyCommission.month == month).all()
        self.assertEqual(len(commissions), 5)
        self.assertEqual(commissions[0].commission_amount, 24000)


if __name__ == '__main__':
    unittest.main()