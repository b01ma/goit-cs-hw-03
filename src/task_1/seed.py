import psycopg2
from faker import Faker
import random

conn = psycopg2.connect (
  host='localhost',
  port=5432,
  database="task_management",
  user="admin",
  password='password123'
)

cur = conn.cursor()

fake = Faker()

try:
  # Add Status
  statuses = ['new', 'in progress', 'completed']
  for status in statuses:
    cur.execute('INSERT INTO status (name) VALUES (%s)', (status,))
    
  # Add usres
  for _ in range (10):
    name = fake.name()
    email = fake.unique.email()
    cur.execute('INSERT INTO users (fullname, email) VALUES (%s, %s)', (name, email))
    
  # Add tasks
  for _ in range (20):
    title = fake.sentence(nb_words=4)[:-1]
    description = fake.text(max_nb_chars=200)
    status_id = random.randint(1,3)
    user_id = random.randint(1,10)
    
    cur.execute(
      "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
      (title, description, status_id, user_id)
    )
    
  conn.commit()
  print('✅ Data successfully added!')
    
except Exception as e:
  print(f"❌ Error: {e}")
  conn.rollback()
  
finally:
  cur.close()
  conn.close()