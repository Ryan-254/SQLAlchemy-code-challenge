# Import necessary modules from your models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review

# Create a SQLAlchemy database engine (SQLite in this example)
engine = create_engine('sqlite:///restaurant_reviews.db')
Base.metadata.create_all(engine)



# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Check if data already exists
if not session.query(Customer).first():
    # Create sample data
    customer1 = Customer(first_name='Catherine', last_name='Mathenge')
    customer2 = Customer(first_name='Christine', last_name='Mathenge')
    restaurant1 = Restaurant(name='Restaurant A', price=4)
    restaurant2 = Restaurant(name='Restaurant B', price=5)
    review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
    review2 = Review(star_rating=5, restaurant=restaurant2, customer=customer2)

    # Add data to the session
    session.add_all([customer1, customer2, restaurant1, restaurant2, review1, review2])

    # Commit the changes to the database
    session.commit()
else:
    print("Sample data already exists in the database.")

# Close the session
session.close()