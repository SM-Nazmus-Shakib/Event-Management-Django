import os
import django
from faker import Faker
import random
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from events.models import Event, Category, RSVP

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

User = get_user_model()

def create_superuser():
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )

def populate_db():
    # Initialize Faker
    fake = Faker()

    # Create superuser if doesn't exist
    create_superuser()

    # Get or create organizer users
    organizers = []
    for i in range(5):
        user, created = User.objects.get_or_create(
            username=f'organizer{i}',
            defaults={
                'email': f'organizer{i}@example.com',
                'password': 'organizer123',
                'is_verified': True
            }
        )
        organizers.append(user)
    print(f"Created {len(organizers)} organizers.")

    # Create Categories
    categories = [
        "Conference", "Workshop", "Seminar", 
        "Social Gathering", "Concert", "Exhibition"
    ]
    category_objs = []
    for name in categories:
        obj, created = Category.objects.get_or_create(
            name=name,
            defaults={'description': fake.paragraph()}
        )
        category_objs.append(obj)
    print(f"Created {len(category_objs)} categories.")

    # Create regular participants
    participants = []
    for i in range(50):
        user, created = User.objects.get_or_create(
            username=f'participant{i}',
            defaults={
                'email': f'participant{i}@example.com',
                'password': 'participant123',
                'is_verified': True
            }
        )
        participants.append(user)
    print(f"Created {len(participants)} participants.")

    # Create Events
    events = []
    for i in range(30):
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
            category=random.choice(category_objs),
            organizer=random.choice(organizers)
        )
        
        # Create RSVPs for participants
        selected_participants = random.sample(participants, random.randint(3, 10))
        for participant in selected_participants:
            RSVP.objects.create(
                user=participant,
                event=event,
                response=random.choice(['YES', 'NO', 'MAYBE'])
            )
        
        events.append(event)
    
    print(f"Created {len(events)} events with RSVPs.")
    print("Database populated successfully!")

if __name__ == '__main__':
    print("Starting database population...")
    populate_db()