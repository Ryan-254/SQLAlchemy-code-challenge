# Import models from separate modules
from models import Restaurant, Customer, Review

# Create a session to interact with the database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create a SQLAlchemy database engine (SQLite in this example)
engine = create_engine('sqlite:///restaurant_reviews.db')
Session = sessionmaker(bind=engine)
session = Session()



class RestaurantReviewer:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.reviews = {}

    def favorite_restaurant(self):
        if not self.reviews:
            return "You haven't reviewed any restaurants yet."
        
        favorite = max(self.reviews, key=self.reviews.get)
        return f"Your favorite restaurant is '{favorite}' with a rating of {self.reviews[favorite]}."

    def add_review(self, restaurant_name, rating):
        if rating < 1 or rating > 5:
            return "Rating must be between 1 and 5."

        # Find the restaurant by name and customer_id
        restaurant = session.query(Restaurant).filter_by(name=restaurant_name).first()
        if not restaurant:
            return f"'{restaurant_name}' does not exist in the database."

        # Check if the customer has already reviewed this restaurant
        existing_review = session.query(Review).filter_by(
            restaurant_id=restaurant.id,
            customer_id=self.customer_id
        ).first()

        if existing_review:
            return f"You have already reviewed '{restaurant_name}'."

        # Create a new review
        new_review = Review(
            star_rating=rating,
            restaurant=restaurant,
            customer_id=self.customer_id
        )
        session.add(new_review)
        session.commit()

        self.reviews[restaurant_name] = rating
        return f"Review added for '{restaurant_name}' with a rating of {rating}."

    def delete_reviews(self, restaurant_name):
        if restaurant_name in self.reviews:
            # Find the restaurant by name and customer_id
            restaurant = session.query(Restaurant).filter_by(name=restaurant_name).first()
            if not restaurant:
                return f"'{restaurant_name}' does not exist in the database."

            # Delete the review
            session.query(Review).filter_by(
                restaurant_id=restaurant.id,
                customer_id=self.customer_id
            ).delete()
            session.commit()

            del self.reviews[restaurant_name]
            return f"Reviews for '{restaurant_name}' have been deleted."
        else:
            return f"You haven't reviewed '{restaurant_name}'."