from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Create the database
engine = create_engine('sqlite:///realestate.db')
Base.metadata.create_all(engine)
