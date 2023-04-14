# Database_Real_Estate

## Usage Guide
#### virtual env and required packages for Linux/Mac
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
##### virtual env and required packages for Windows
```
python3 -m venv venv
venv\Scripts\activate
pip3 install -r requirements.txt
```
#### Creating the Data Base, Insering fake data, Querying the data
```
python3 create.py
python3 insert.py
python3 queries.py
```
#### Running Tests
```
python3 test.py
```
## Table Schema
- Office: Represents the offices with columns: office_id (primary key), address, city, state, and zip_code.

- EstateAgent: Represents the gents with columns: agent_id (primary key), first_name, last_name, email (unique), and phone (unique).

- AgentOffice: Represents the relationship between the agents and offices with columns: agent_office_id (primary key), agent_id (foreign key to estate_agents.agent_id), and office_id (foreign key to offices.office_id).

- Seller: Represents the house sellers with columns: seller_id (primary key), name, email (unique), and phone (unique).

- Listing: Represents the house listings with columns: listing_id (primary key), seller_id (foreign key to sellers.seller_id), bedrooms, bathrooms, listing_price, zip_code, date_of_listing, agent_id (foreign key to estate_agents.agent_id), office_id (foreign key to offices.office_id), and status.

- Buyer: Represents the house buyers with columns: buyer_id (primary key), name, email (unique), and phone (unique).

- Sale: Represents the house sales with columns: sale_id (primary key), listing_id (foreign key to listings.listing_id), buyer_id (foreign key to buyers.buyer_id), sale_price, date_of_sale, and agent_id (foreign key to estate_agents.agent_id).

- Commission: Represents the commissions received by agents with columns: commission_id (primary key), agent_id (foreign key to estate_agents.agent_id), sale_id (foreign key to sales.sale_id), commission_amount, and commission_date.

- MonthlyCommission: Represents the monthly commissions for agents with columns: monthly_commission_id (primary key), agent_id (foreign key to estate_agents.agent_id), year, month, and total_commission.

## Indexing

To increase the performance of these queries that run every month, we should create suitable indexes for the database tables.

Explanation:

-  ``get_top_offices()``: Obtains the top 5 offices with the highest sales in a specified month. It connects the Office, Listing, and Sale tables and filters the outcomes by the year and month of the sale. The main filter is on the date_of_sale column.

-  ``get_top_agents()``: Retrieves the top 5 agents with the highest sales in a particular month. It joins the EstateAgent and Sale tables and filters the results by the year and month of the sale. The main filter is on the ``date_of_sale`` column.

-  ``get_average_days_on_market()``: Computes the average number of days a listing remains on the market before being sold in a specific month. It links the Listing and Sale tables and filters the outcomes by the year and month of the sale. The primary filter is on the ``date_of_sale`` column.

-  ``get_average_selling_price()``: Calculates the average selling price of listings in a certain month. It filters the Sale table by the year and month of the sale. The primary filter is on the date_of_sale column.

-  ``insert_monthly_commissions()``: Gathers the total commission amount for each agent in a given month. It joins the Commission and Sale tables and filters the results by the year and month of the sale. The primary filter is on the date_of_sale column.

The date_of_sale column is used in most queries. So, we create a first-order index on the date_of_sale column in the Sale table:

```
date_of_sale = Column(Date, index=True)
```
Also, the Office and Listing tables are connected in the ``get_top_offices()`` query. So, we can create a first-order index on the ``office_id`` column in the Listing table:

```
office_id = Column(Integer, ForeignKey('offices.office_id'), index=True)
```
The EstateAgent and Sale tables are joined in the ``get_top_agents()`` query. So, we can create a first-order index on the ``agent_id`` column in the Sale table:

```
agent_id = Column(Integer, ForeignKey('estate_agents.agent_id'), index=True)
```

Second-order indexing is not required because there are no queries with multiple filter conditions that would benefit from composite indexes.


## Transactions
Transactions are used so that a group of SQL operations get executed as an atomic unit of work. So, either all the operations are executed successfully or none. 
- ``generate_listings_and_sellers()`` function
    - the code is adding a seller and listing object to the session and if any error happens during this process, the transaction is rolled back. (to make sure that the database remains consistent and that partial changes are not committed.)

## Normalization

### First Normal Form (1NF):
- Each table has a primary key
    - Office: office_id
    - EstateAgent: agent_id
    - AgentOffice: agent_office_id
    - Seller: seller_id
    - Listing: listing_id
    - Buyer: buyer_id
    - Sale: sale_id
    - Commission: commission_id
- All columns have atomic values.
- There is no multi-valued attributes (the many-to-many relationship between Office and EstateAgent is handled by the AgentOffice junction table).
### Second Normal Form (2NF):

- All tables are already in 1NF.
- All non-key attributes are fully dependent on the primary key.
- In each table, every non-key attribute depends on the primary key and not on a subset of the primary key.
### Third Normal Form (3NF):

- All tables are already in 2NF.
- Transitive dependencies have been removed by creating separate tables for Seller, Buyer, and the junction table AgentOffice.
    - For example, in the original schema, Listing included seller_name, seller_email, and seller_phone. By creating the Seller table, we have removed the transitive dependency between Listing and seller details.
- Unique constraints have been added to non-key attributes that should be unique, such as email and phone in EstateAgent, Seller, and Buyer classes.
### Fourth Normal Form (4NF):

- All tables are already in 3NF.
There are no multi-valued dependencies. (The many-to-many relationship between Office and EstateAgent is handled by the AgentOffice junction table, ensuring that the schema is in 4NF.)


Overall, the schema has been designed to follow all four normalization rules by ensuring each table has a primary key, atomic values, full dependency on the primary key, no transitive dependencies, and no multi-valued dependencies.