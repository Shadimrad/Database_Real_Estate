import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta, date
from create import Base, Office, EstateAgent, Listing, Sale, Commission, MonthlyCommission, AgentOffice, Seller, Buyer
from queries import get_top_offices, get_top_agents, get_average_days_on_market, get_average_selling_price, insert_monthly_commissions, print_monthly_commissions

class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        """
        Set up the database and create sample data.
        """
        self.engine = create_engine("sqlite:///:memory:") # Create an in-memory database
        Base.metadata.create_all(self.engine) # Create all tables
        Session = sessionmaker(bind=self.engine) # Create a session
        self.session = Session()

        # Create sample data and add it to the session
        self.create_sample_data()

    def tearDown(self):
        """
        Close the session and drop all tables.
        """
        self.session.close() # Close the session
        Base.metadata.drop_all(self.engine) # Drop all tables
        self.engine.dispose() # Dispose of the engine

    def create_sample_data(self):
        """
        Create sample data.
        """
        offices = [
            Office(office_id=1, address="Address 1", city="City 1", state="State 1", zip_code="ZipCode1"),
            Office(office_id=2, address="Address 2", city="City 2", state="State 2", zip_code="ZipCode2"),
            Office(office_id=3, address="Address 3", city="City 3", state="State 3", zip_code="ZipCode3"),
            Office(office_id=4, address="Address 4", city="City 4", state="State 4", zip_code="ZipCode4"),
            Office(office_id=5, address="Address 5", city="City 5", state="State 5", zip_code="ZipCode5"),
            Office(office_id=6, address="Address 6", city="City 6", state="State 6", zip_code="ZipCode6")
        ]

        agents = [
            EstateAgent(agent_id=1, first_name="FirstName1", last_name="LastName1", email="email1@example.com", phone="Phone1"),
            EstateAgent(agent_id=2, first_name="FirstName2", last_name="LastName2", email="email2@example.com", phone="Phone2"),
            EstateAgent(agent_id=3, first_name="FirstName3", last_name="LastName3", email="email3@example.com", phone="Phone3"),
            EstateAgent(agent_id=4, first_name="FirstName4", last_name="LastName4", email="email4@example.com", phone="Phone4"),
            EstateAgent(agent_id=5, first_name="FirstName5", last_name="LastName5", email="email5@example.com", phone="Phone5"),
            EstateAgent(agent_id=6, first_name="FirstName6", last_name="LastName6", email="email6@exmaple.com", phone="Phone6")
        ]

        sellers = [
            Seller(seller_id=1, name="SellerName1", email="selleremail1@example.com", phone="SellerPhone1"),
            Seller(seller_id=2, name="SellerName2", email="selleremail2@example.com", phone="SellerPhone2"),
            Seller(seller_id=3, name="SellerName3", email="selleremail3@example.com", phone="SellerPhone3"),
            Seller(seller_id=4, name="SellerName4", email="selleremail4@example.com", phone="SellerPhone4"),
            Seller(seller_id=5, name="SellerName5", email="selleremail5@example.com", phone="SellerPhone5"),
            Seller(seller_id=6, name="SellerName6", email="selleremail6@example.com", phone="SellerPhone6")
        ]

        listings = [
            Listing(listing_id=1, seller_id=1, bedrooms=2, bathrooms=1, listing_price=200000, zip_code="ZipCode1",
                    date_of_listing=date.today() - timedelta(days=1), agent_id=1, office_id=1, status="sold"),
            Listing(listing_id=2, seller_id=2, bedrooms=3, bathrooms=2, listing_price=300000, zip_code="ZipCode2",
                    date_of_listing=date.today() - timedelta(days=2), agent_id=1, office_id=1, status="sold"),
            Listing(listing_id=3, seller_id=3, bedrooms=4, bathrooms=3, listing_price=400000, zip_code="ZipCode3",
                    date_of_listing=date.today() - timedelta(days=3), agent_id=1, office_id=4, status="sold"),
            Listing(listing_id=4, seller_id=4, bedrooms=5, bathrooms=4, listing_price=500000, zip_code="ZipCode4",
                    date_of_listing=date.today() - timedelta(days=4), agent_id=2, office_id=2, status="sold"),
            Listing(listing_id=5, seller_id=5, bedrooms=6, bathrooms=5, listing_price=600000, zip_code="ZipCode5",
                    date_of_listing=date.today() - timedelta(days=5), agent_id=2, office_id=2, status="sold"),
            Listing(listing_id=6, seller_id=6, bedrooms=7, bathrooms=6, listing_price=700000, zip_code="ZipCode6",
                    date_of_listing=date.today() - timedelta(days=6), agent_id=2, office_id=6, status="sold"),
            Listing(listing_id=7, seller_id=1, bedrooms=8, bathrooms=7, listing_price=800000, zip_code="ZipCode1",
                    date_of_listing=date.today() - timedelta(days=7), agent_id=3, office_id=6, status="sold"),
            Listing(listing_id=8, seller_id=2, bedrooms=9, bathrooms=8, listing_price=900000, zip_code="ZipCode2",
                    date_of_listing=date.today() - timedelta(days=8), agent_id=3, office_id=6, status="sold"),
            Listing(listing_id=9, seller_id=3, bedrooms=10, bathrooms=9, listing_price=1000000, zip_code="ZipCode3",
                    date_of_listing=date.today() - timedelta(days=9), agent_id=3, office_id=3, status="sold"),
            Listing(listing_id=10, seller_id=4, bedrooms=11, bathrooms=10, listing_price=1100000, zip_code="ZipCode4",
                    date_of_listing=date.today() - timedelta(days=10), agent_id=4, office_id=5, status="sold")
            
            
        ]

        buyers = [
            Buyer(buyer_id=1, name="BuyerName1", email="buyeremail1@example.com", phone="BuyerPhone1"),
            Buyer(buyer_id=2, name="BuyerName2", email="buyeremail2@example.com", phone="BuyerPhone2")
        ]

        sales = [
            Sale(sale_id=1, listing_id=1, buyer_id=1, sale_price=195000, date_of_sale=date.today() - timedelta(days=1), agent_id=1),
            Sale(sale_id=2, listing_id=2, buyer_id=2, sale_price=290000, date_of_sale=date.today() - timedelta(days=0), agent_id=2),
            Sale(sale_id=3, listing_id=3, buyer_id=1, sale_price=390000, date_of_sale=date.today() - timedelta(days=2), agent_id=1),
            Sale(sale_id=4, listing_id=4, buyer_id=2, sale_price=490000, date_of_sale=date.today() - timedelta(days=3), agent_id=2),
            Sale(sale_id=5, listing_id=5, buyer_id=1, sale_price=590000, date_of_sale=date.today() - timedelta(days=4), agent_id=1),
            Sale(sale_id=6, listing_id=6, buyer_id=2, sale_price=690000, date_of_sale=date.today() - timedelta(days=5), agent_id=2),
            Sale(sale_id=7, listing_id=7, buyer_id=1, sale_price=790000, date_of_sale=date.today() - timedelta(days=6), agent_id=3),
            Sale(sale_id=8, listing_id=8, buyer_id=2, sale_price=890000, date_of_sale=date.today() - timedelta(days=7), agent_id=3),
            Sale(sale_id=9, listing_id=9, buyer_id=1, sale_price=990000, date_of_sale=date.today() - timedelta(days=8), agent_id=3),
            Sale(sale_id=10, listing_id=10, buyer_id=2, sale_price=1090000, date_of_sale=date.today() - timedelta(days=9), agent_id=4),
            Sale(sale_id=11, listing_id=1, buyer_id=1, sale_price=195000, date_of_sale=date.today() - timedelta(days=1), agent_id=1),
            Sale(sale_id=12, listing_id=2, buyer_id=2, sale_price=290000, date_of_sale=date.today() - timedelta(days=0), agent_id=2),
            Sale(sale_id=13, listing_id=3, buyer_id=1, sale_price=390000, date_of_sale=date.today() - timedelta(days=2), agent_id=1),
            Sale(sale_id=14, listing_id=4, buyer_id=2, sale_price=490000, date_of_sale=date.today() - timedelta(days=3), agent_id=2),
            Sale(sale_id=15, listing_id=5, buyer_id=1, sale_price=590000, date_of_sale=date.today() - timedelta(days=4), agent_id=1),
            Sale(sale_id=16, listing_id=6, buyer_id=2, sale_price=690000, date_of_sale=date.today() - timedelta(days=5), agent_id=2)

        ]

        commissions = [
            Commission(commission_id=1, agent_id=1, sale_id=1, commission_amount=3900, commission_date=date.today() - timedelta(days=1)),
            Commission(commission_id=2, agent_id=2, sale_id=2, commission_amount=5800, commission_date=date.today() - timedelta(days=1)),
            Commission(commission_id=3, agent_id=1, sale_id=3, commission_amount=7800, commission_date=date.today() - timedelta(days=2)),
            Commission(commission_id=4, agent_id=2, sale_id=4, commission_amount=9700, commission_date=date.today() - timedelta(days=2)),
            Commission(commission_id=5, agent_id=1, sale_id=5, commission_amount=11700, commission_date=date.today() - timedelta(days=2)),
            Commission(commission_id=6, agent_id=2, sale_id=6, commission_amount=13600, commission_date=date.today() - timedelta(days=3)),
            Commission(commission_id=7, agent_id=3, sale_id=7, commission_amount=15600, commission_date=date.today() - timedelta(days=3)),
            Commission(commission_id=8, agent_id=3, sale_id=8, commission_amount=17500, commission_date=date.today() - timedelta(days=4)),
            Commission(commission_id=9, agent_id=3, sale_id=9, commission_amount=19500, commission_date=date.today() - timedelta(days=4))
        ]

        monthly_commissions = [
            MonthlyCommission(monthly_commission_id=1, agent_id=1, year=date.today().year, month=date.today().month, total_commission=3900),
            MonthlyCommission(monthly_commission_id=2, agent_id=2, year=date.today().year, month=date.today().month, total_commission=5800),
            MonthlyCommission(monthly_commission_id=3, agent_id=3, year=date.today().year, month=date.today().month, total_commission=15600),
            MonthlyCommission(monthly_commission_id=4, agent_id=4, year=date.today().year, month=date.today().month, total_commission=0),
            MonthlyCommission(monthly_commission_id=5, agent_id=1, year=date.today().year, month=date.today().month, total_commission=11700),
            MonthlyCommission(monthly_commission_id=6, agent_id=2, year=date.today().year, month=date.today().month, total_commission=13600),
            MonthlyCommission(monthly_commission_id=7, agent_id=3, year=date.today().year, month=date.today().month - 1, total_commission=19500)

        ]

        for obj in offices + agents + sellers + listings + buyers + sales + commissions + monthly_commissions:
            self.session.add(obj)

        self.session.commit()


    def test_get_top_offices(self):
        """
        Test that the get_top_offices function returns the correct output for the given input
        """
        top_offices = get_top_offices(self.session, date.today().year, date.today().month)
        expected_output = [(6, 'City 6', 'State 6', 4),
                           (2, 'City 2', 'State 2', 4),
                           (1, 'City 1', 'State 1', 4),
                           (4, 'City 4', 'State 4', 2),
                           (5, 'City 5', 'State 5', 1)]
        self.assertEqual(top_offices, expected_output) # Check that the output is correct based on the data

    def test_get_top_agents(self):
        """
        Test that the get_top_agents function returns the correct output for the given input
        """
        top_agents = get_top_agents(self.session, date.today().year, date.today().month)
        # Extract agent_id of each tuple of agent_id and the numebr of sales in the top_agents list
        top_agents_ids = [agent[0].agent_id for agent in top_agents]
        expected_output = [2,1,3,4]
        self.assertEqual(top_agents_ids, expected_output)



    def test_get_average_days_on_market(self):
        """
        Test that the get_average_days_on_market function returns the correct output for the given input
        """
        average_days_on_market = get_average_days_on_market(self.session, date.today().year, date.today().month)
        expected_output = 0.0
        self.assertEqual(average_days_on_market, expected_output)

    def test_get_average_selling_price(self):
        """
        Test that the get_average_selling_price function returns the correct output for the given input
        """
        average_selling_price = get_average_selling_price(self.session, date.today().year, date.today().month)
        expected_output = 565625.0
        self.assertEqual(average_selling_price, expected_output)

    def test_insert_monthly_commissions(self):
        """
        Test that the insert_monthly_commissions function returns the correct output for the given input
        """
        monthly_commissions = insert_monthly_commissions(self.session, date.today().year, date.today().month)
        expected_output = [
            (1, 23400.0), (2, 29100.0), (3, 52600.0)
        ]
        self.assertEqual(monthly_commissions, expected_output)




if __name__ == '__main__':
    unittest.main()
