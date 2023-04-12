from datetime import date
from sqlalchemy import func, extract
from create import Office, EstateAgent, Listing, Sale, Commission, MonthlyCommission

def get_top_offices(session, year, month):
    top_offices = (
        session.query(Office.office_id, Office.city, Office.state, func.count(Sale.sale_id).label("sales_count"))
        .join(Listing, Listing.office_id == Office.office_id)
        .join(Sale, Sale.listing_id == Listing.listing_id)
        .filter(extract("year", Sale.date_of_sale) == year)
        .filter(extract("month", Sale.date_of_sale) == month)
        .group_by(Office.office_id)
        .order_by(func.count(Sale.sale_id).desc())
        .limit(5)
    ).all()
    return top_offices

def get_top_agents(session, year, month):
    top_agents = (
        session.query(EstateAgent, func.count(Sale.sale_id).label("sales_count"))
        .join(Sale, Sale.agent_id == EstateAgent.agent_id)
        .filter(extract("year", Sale.date_of_sale) == year)
        .filter(extract("month", Sale.date_of_sale) == month)
        .group_by(EstateAgent.agent_id)
        .order_by(func.count(Sale.sale_id).desc())
        .limit(5)
    ).all()
    return top_agents

def get_average_days_on_market(session, year, month):
    average_days_on_market = (
        session.query(func.avg(Sale.date_of_sale - Listing.date_of_listing).label("average_days_on_market"))
        .join(Listing, Listing.listing_id == Sale.listing_id)
        .filter(extract("year", Sale.date_of_sale) == year)
        .filter(extract("month", Sale.date_of_sale) == month)
    ).scalar()
    return average_days_on_market

def get_average_selling_price(session, year, month):
    average_selling_price = (
        session.query(func.avg(Sale.sale_price).label("average_selling_price"))
        .filter(extract("year", Sale.date_of_sale) == year)
        .filter(extract("month", Sale.date_of_sale) == month)
    ).scalar()
    return average_selling_price

def insert_monthly_commissions(session, year, month):
    monthly_commissions = (
        session.query(
            Commission.agent_id,
            func.sum(Commission.commission_amount).label("total_commission")
        )
        .join(Sale, Sale.sale_id == Commission.sale_id)
        .filter(extract("year", Sale.date_of_sale) == year)
        .filter(extract("month", Sale.date_of_sale) == month)
        .group_by(Commission.agent_id)
    ).all()

    for agent_id, total_commission in monthly_commissions:
        monthly_commission = MonthlyCommission(
            agent_id=agent_id,
            year=year,
            month=month,
            total_commission=total_commission
        )
        session.add(monthly_commission)

    session.commit()

# Example usage
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine("sqlite:///realestate.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    current_year = date.today().year
    current_month = date.today().month

    top_offices = get_top_offices(session, current_year, current_month)
    top_agents = get_top_agents(session, current_year, current_month)
    average_days_on_market = get_average_days_on_market(session, current_year, current_month)
    average_selling_price = get_average_selling_price(session, current_year, current_month)

    print("Top 5 Offices with the most sales for the month:")
    for office in top_offices:
        print(f"Office ID: {office.office_id}, City: {office.city}, State: {office.state}, Sales: {office.sales_count}")

    print("\nTop 5 Estate Agents who have sold the most for the month:")
    for agent, sales_count in top_agents:
        print(f"Agent ID: {agent.agent_id}, Name: {agent.first_name} {agent.last_name}, Email: {agent.email}, Phone: {agent.phone}, Sales: {sales_count}")

    print(f"\nAverage number of days on the market: {average_days_on_market}")
    print(f"Average selling price: ${average_selling_price:,.2f}")
