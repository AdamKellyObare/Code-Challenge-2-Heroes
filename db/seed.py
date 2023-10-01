from app import db
from app.models import Hero, Powers, HeroPowers
import random

# In order the Seeding Process to start, write the following
print("🦸‍♀️ Seeding powers...")

# This is an array of dictionary objects, each rep a power

powers_data = [
    {"power_name": "super strength"},
    {"power_name": "flight"},
    {"power_name": "super human senses"},
    {"power_name": "elasticity"}
]

# Iterate over over the array above and instert each power into the powers table
for power in powers_data:
    new_power = Powers(**power)
    # this adds the new power object to the db sesson
    db.session.add(new_power)
# this commits the current db session and saves the changes made
db.session.commit()

# prints out to indicate starting of seeding process
print("🦸‍♀️ Seeding heroes...")
# array of dictionary objects, each rep a Hero
heroes_data = [
   {"name":"Kamala Khan"},
   {"name":"Doreen Green"},
   {"name":"Gwen Stacy"},
   {"name":"Janet Van Dyne"},
   {"name":"Wanda Maximoff"},
   {"name":"Carol Danvers"},
   {"name":"Jean Grey"},
   {"name":"Ororo Munroe"},
   {"name":"Kitty Pryde"},
   {"name":"Elektra Natchios"}
]

# Iterate over the arrayand insert each hero into the Heroes Table

for hero in heroes_data:
    new_hero = Hero(**hero)
    # adds new hero object to the db session
    db.session.add(new_hero)

# commits the current db session and saves the changes that are made
db.session.commit()

# prints out to show the process of adding powers to heroes
print("🦸‍♀️ Adding powers to heroes...")
# defining  strengths each hero can have
strengths = ["Strong", "Weak", "Average"]
#fetching all records from the Heroes and Powers table
all_heroes = Hero.query.all()
all_powers = Powers.query.all()
#assigning powers to all heroes
for hero in all_heroes:
    for _ in range(random.randint(1, 3)):
        power = random.choice(all_powers)
        strength = random.choice(strengths)
        hero_power = HeroPowers(hero_id=hero.id, power_id=power.id, strength=strength)
        db.session.add(hero_power)
db.session.commit()

print("🦸‍♀️ Done seeding!")
