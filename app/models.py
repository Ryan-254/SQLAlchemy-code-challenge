from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy database engine (SQLite in this example)
engine = create_engine('sqlite:///restaurant_reviews.db')
Base = declarative_base()

# Import your models from separate modules
from .restaurants import Restaurant
from customer import Customer
from review import Review

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()