from app import app
from models import User, db

def seed_database():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create test users
    user1 = User(username="testuser1", email="testuser1@example.com", password="password1")
    user2 = User(username="testuser2", email="testuser2@example.com", password="password2")
    user3 = User(username="testuser3", email="testuser3@example.com", password="password3")

    # Add test users to the session
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    # Commit the session
    db.session.commit()

    # Print a message to indicate the seeding process is complete
    print("Database seeded with test users.")

if __name__ == "__main__":
    with app.app_context():
        seed_database()
