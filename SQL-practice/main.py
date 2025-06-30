import pgdb
from dotenv import load_dotenv
import os
load_dotenv()
pg_password = os.getenv("PASSWORD")
connection = pgdb.connect(
    database='world',
    host='localhost',
    user='postgres',
    password=pg_password,
    port=5432
)

curser = connection.cursor()

try:
    curser.execute("SELECT * FROM capitals")
    quiz = curser.fetchall()
    for row in quiz:
        print(row)

except Exception as err:
    print("Error executing query:", err)

finally:
    curser.close()
    connection.close()