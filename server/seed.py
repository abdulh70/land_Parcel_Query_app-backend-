from app import app
from models import db

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
      from server.app import db
from server.models import User, LandQuery

def seed_db():
    user = User(username='testuser', email='testuser@example.com', password_hash='hashedpassword')
    db.session.add(user)
    db.session.commit()

    query = LandQuery(query_text='Interested in buying land in XYZ area.', user_id=user.id)
    db.session.add(query)
    db.session.commit()

if __name__ == '__main__':
    seed_db()