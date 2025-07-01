import os
import django
from faker import Faker
import random
from datetime import datetime, timedelta
from events.models import Event, Participant, Category

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create Categories
    categories = [
        "Conference", "Workshop", "Seminar", 
        "Social Gathering", "Concert", "Exhibition"
    ]
    category_objs = [Category.objects.create(
        name=name,
        description=fake.paragraph()
    ) for name in categories]
    print(f"Created {len(category_objs)} categories.")

    # Create Participants
    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.unique.email()
    ) for _ in range(50)]
    print(f"Created {len(participants)} participants.")

    # Create Events
    events = []
    for _ in range(30):
        start_date = fake.date_between_dates(
            date_start=datetime.now() - timedelta(days=30),
            date_end=datetime.now() + timedelta(days=60)
        )
        
        event = Event.objects.create(
            name=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=5),
            date=start_date,
            time=fake.time_object(),
            location=fake.address(),
            category=random.choice(category_objs)
        )
        
        # Assign random participants (3-10 per event)
        event.participants.set(random.sample(participants, random.randint(3, 10)))
        events.append(event)
    
    print(f"Created {len(events)} events with participants.")
    print("Database populated successfully!")

if __name__ == '__main__':
    print("Starting database population...")
    populate_db()