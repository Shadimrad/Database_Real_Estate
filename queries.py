# SQL queries for generating monthly reports
from datetime import date
from sqlalchemy import func, extract
from create import Office, EstateAgent, Listing, Sale
from insert import session


# Assuming you want to generate the reports for the current month
current_year = date.today().year
current_month = date.today().month

# 1. Find the top 5 offices with the most sales for that month
top_offices = (
    session.query(Office.office_id, Office.city, Office.state, func.count(Sale.sale_id).label("sales_count"))
    .join(Listing, Listing.office_id == Office.office_id)
    .join(Sale, Sale.listing_id == Listing.listing_id)
    .filter(extract("year", Sale.date_of_sale) == current_year)
    .filter(extract("month", Sale.date_of_sale) == current_month)
    .group_by(Office.office_id)
    .order_by(func.count(Sale.sale_id).desc())
    .limit(5)
).all()

# 2. Find the top 5 estate agents who have sold the most for the month
top_agents = (
    session.query(EstateAgent, func.count(Sale.sale_id).label("sales_count"))
    .join(Sale, Sale.agent_id == EstateAgent.agent_id)
    .filter(extract("year", Sale.date_of_sale) == current_year)
    .filter(extract("month", Sale.date_of_sale) == current_month)
    .group_by(EstateAgent.agent_id)
    .order_by(func.count(Sale.sale_id).desc())
    .limit(5)
).all()

# 3. Calculate the commission that each estate agent must receive and store the results in a separate table
# This is already done in the insert.py file when inserting data for Sales.

# 4. For all houses that were sold that month, calculate the average number of days on the market
average_days_on_market = (
    session.query(func.avg(Sale.date_of_sale - Listing.date_of_listing).label("average_days_on_market"))
    .join(Listing, Listing.listing_id == Sale.listing_id)
    .filter(extract("year", Sale.date_of_sale) == current_year)
    .filter(extract("month", Sale.date_of_sale) == current_month)
).scalar()

# 5. For all houses that were sold that month, calculate the average selling price
average_selling_price = (
    session.query(func.avg(Sale.sale_price).label("average_selling_price"))
    .filter(extract("year", Sale.date_of_sale) == current_year)
    .filter(extract("month", Sale.date_of_sale) == current_month)
).scalar()

print("Top 5 Offices with the most sales for the month:")
for office in top_offices:
    print(f"Office ID: {office.office_id}, City: {office.city}, State: {office.state}, Sales: {office.sales_count}")

print("\nTop 5 Estate Agents who have sold the most for the month:")
for agent, sales_count in top_agents:
    print(f"Agent ID: {agent.agent_id}, Name: {agent.first_name} {agent.last_name}, Email: {agent.email}, Phone: {agent.phone}, Sales: {sales_count}")

print(f"\nAverage number of days on the market: {average_days_on_market}")
print(f"Average selling price: ${average_selling_price:,.2f}")
