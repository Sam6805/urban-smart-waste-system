import random
from faker import Faker
import mysql.connector
from datetime import date
from Website.models import get_db_connection


fake = Faker("en_IN")

db = get_db_connection()

cur = db.cursor()

areas = [
"Anand Nagar", "Bhagay Nagar", "Shree Nagar", "Shivaji Nagar", "Vijay Nagar",
"Kabara Nagar", "Namaskar chauk", "Hanuman peth", "Ganesh Nagar", "Sham Nagar"
]

vehicle_numbers = [
    "KA01AB1234", "KA02CD5678", "KA03EF9012",
    "KA04GH3456", "KA05JK7890", "KA06LM4321"
]

for i in range(2):

    name = fake.name()
    phone = fake.numerify(text="##########")
    password = fake.password()
    vehicle = random.choice(vehicle_numbers)
    area = random.choice(areas)
    isActive = random.choice([0, 1])
    total_collected = random.randint(0, 50)
    cdate = fake.date_between(start_date=date(2025, 1, 1), end_date=date(2025, 12, 12))
    last_active = fake.date_between(start_date=date(2025, 1, 1), end_date=date(2025, 12, 12))

    sql = """
    INSERT INTO collector (name, phone_no, password, vehicle_no, area, isActive, total_collected, createdAt, lastActive)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    val = (name, phone, password, vehicle, area, isActive, total_collected, cdate, last_active)
    cur.execute(sql, val)

db.commit()
print("Inserted 2 Indian collectors!")

