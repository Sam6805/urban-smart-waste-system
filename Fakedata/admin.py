from faker import Faker
import mysql.connector
import random
from Website.models import get_db_connection

fake = Faker("en_IN") 

db = get_db_connection()

cur = db.cursor()

areas = [
"Anand Nagar", "Bhagay Nagar", "Shree Nagar", "Shivaji Nagar", "Vijay Nagar",
"Kabara Nagar", "Namaskar chauk", "Hanuman peth", "Ganesh Nagar", "Sham Nagar"
]

for i in range(3):
    name = fake.name()
    email = fake.email()
    phone = fake.numerify(text="##########")
    password = fake.password(length=8)
    address = random.choice(areas)

    sql = "INSERT INTO admin (name,email, phone_no, password, address) VALUES (%s,%s, %s, %s, %s)"
    val = ( name,email, phone, password, address)

    cur.execute(sql, val)

db.commit()
print("Inserted 3 Indian users!")